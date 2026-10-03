"""Tool behavior: ID parsing, result shaping, dry_run, and schema/annotations as seen over MCP."""

import httpx
import pytest
from fastmcp import Client

import notion_api
from notion_api import NotionAPIError
from server import mcp

PAGE_ID = "3ec932b1-ff5f-8063-81bb-d15f413710fc"


@pytest.fixture
def fake_notion(monkeypatch):
    """Route httpx.request to a handler keyed by (method, path suffix); record every call."""
    state = {"routes": {}, "calls": []}

    def fake_request(method, url, **kwargs):
        state["calls"].append((method, url))
        for (route_method, suffix), body in state["routes"].items():
            if method == route_method and url.endswith(suffix):
                return httpx.Response(200, json=body)
        raise AssertionError(f"unexpected request {method} {url}")

    monkeypatch.setattr(notion_api.httpx, "request", fake_request)
    monkeypatch.setattr(notion_api, "get_token", lambda: "test-token")
    return state


@pytest.mark.parametrize(
    "value",
    [
        PAGE_ID,
        PAGE_ID.replace("-", ""),
        "https://app.notion.com/p/MCP-Sandbox-3ec932b1ff5f806381bbd15f413710fc",
        "https://app.notion.com/p/3ec932b1ff5f806381bbd15f413710fc",
        "https://www.notion.so/MCP-Sandbox-3ec932b1ff5f806381bbd15f413710fc?pvs=4#abc",
        f"  {PAGE_ID.upper()}  ",
    ],
)
def test_normalize_page_id_accepts_ids_and_urls(value):
    assert notion_api.normalize_page_id(value) == PAGE_ID


def test_normalize_page_id_rejects_garbage():
    with pytest.raises(NotionAPIError) as exc:
        notion_api.normalize_page_id("a")
    assert exc.value.error == "validation_error"
    assert "search_pages" in exc.value.hint


def test_search_shapes_parents_and_has_more(fake_notion):
    def page(page_id, parent):
        return {
            "id": page_id,
            "url": f"https://app.notion.com/p/{page_id}",
            "last_edited_time": "2026-10-01T00:00:00.000Z",
            "parent": parent,
            "properties": {"title": {"type": "title", "title": [{"plain_text": "T"}]}},
        }

    fake_notion["routes"][("POST", "/search")] = {
        "results": [
            page("a", {"type": "workspace", "workspace": True}),
            page("b", {"type": "page_id", "page_id": "parent-page"}),
            page("c", {"type": "data_source_id", "data_source_id": "parent-db"}),
        ],
        "has_more": True,
    }
    result = notion_api.search_pages("T")
    parents = [(r["parent_type"], r["parent_id"]) for r in result["results"]]
    assert parents == [("workspace", None), ("page", "parent-page"), ("database", "parent-db")]
    assert result["has_more"] is True


def test_dry_run_previews_without_writing(fake_notion):
    lines = [f"line {i}" for i in range(15)]
    fake_notion["routes"][("GET", f"/pages/{PAGE_ID}")] = {
        "id": PAGE_ID,
        "properties": {"title": {"type": "title", "title": [{"plain_text": "Sandbox"}]}},
    }
    fake_notion["routes"][("GET", f"/pages/{PAGE_ID}/markdown")] = {
        "markdown": "\n".join(lines),
        "truncated": False,
    }

    preview = notion_api.append_to_page(PAGE_ID, "## New", dry_run=True)

    assert preview["dry_run"] is True
    assert preview["title"] == "Sandbox"
    assert preview["current_ending"] == "\n".join(lines[-notion_api.PREVIEW_LINES :])
    assert preview["will_append"] == "## New"
    assert all(method == "GET" for method, _ in fake_notion["calls"])


# ---- Through the MCP protocol (in-memory client, no network) ----


@pytest.mark.anyio
async def test_limit_out_of_range_rejected_before_notion(fake_notion):
    async with Client(mcp) as client:
        result = await client.call_tool(
            "search_pages", {"query": "x", "limit": 500}, raise_on_error=False
        )
    assert result.is_error
    assert "less than or equal to 100" in result.content[0].text
    assert fake_notion["calls"] == []


@pytest.mark.anyio
async def test_schemas_and_annotations_visible_to_agent():
    async with Client(mcp) as client:
        tools = {tool.name: tool for tool in await client.list_tools()}

    limit = tools["search_pages"].input_schema["properties"]["limit"]
    assert (limit["minimum"], limit["maximum"]) == (1, 100)
    assert tools["search_pages"].annotations.read_only_hint is True
    assert tools["read_page"].annotations.read_only_hint is True
    append = tools["append_to_page"]
    assert append.annotations.read_only_hint is False
    assert append.annotations.idempotent_hint is False
    assert append.input_schema["properties"]["dry_run"]["default"] is False
    assert "has_more" in tools["search_pages"].output_schema["properties"]
