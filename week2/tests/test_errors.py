"""Error classification and retry policy in notion_api._request. No network: httpx is faked."""

import httpx
import pytest

import notion_api
from notion_api import NotionAPIError

PAGE_ID = "3ec932b1-ff5f-8063-81bb-d15f413710fc"


@pytest.fixture
def fake_notion(monkeypatch):
    """Replace httpx.request with a queue of canned responses; record calls and sleeps."""
    state = {"responses": [], "calls": 0, "sleeps": []}

    def fake_request(method, url, **kwargs):
        state["calls"] += 1
        status, body, headers = state["responses"].pop(0)
        return httpx.Response(status, json=body, headers=headers)

    monkeypatch.setattr(notion_api.httpx, "request", fake_request)
    monkeypatch.setattr(notion_api.time, "sleep", state["sleeps"].append)
    monkeypatch.setattr(notion_api, "get_token", lambda: "test-token")
    return state


def _error_body(code, message="boom"):
    return {"object": "error", "code": code, "message": message}


def test_read_retries_5xx_then_succeeds(fake_notion):
    fake_notion["responses"] = [
        (503, _error_body("service_unavailable"), {}),
        (503, _error_body("service_unavailable"), {}),
        (200, {"results": []}, {}),
    ]
    assert notion_api.search_pages("anything") == []
    assert fake_notion["calls"] == 3
    assert len(fake_notion["sleeps"]) == 2


def test_write_is_not_retried_on_5xx(fake_notion):
    fake_notion["responses"] = [(503, _error_body("service_unavailable"), {})]
    with pytest.raises(NotionAPIError) as exc:
        notion_api.append_to_page(PAGE_ID, "hello")
    assert fake_notion["calls"] == 1
    assert exc.value.retryable is True
    assert "read_page" in exc.value.hint


def test_write_is_retried_on_429(fake_notion):
    fake_notion["responses"] = [
        (429, _error_body("rate_limited"), {"Retry-After": "1"}),
        (200, {"id": PAGE_ID}, {}),
    ]
    result = notion_api.append_to_page(PAGE_ID, "hello")
    assert result["status"] == "appended"
    assert fake_notion["calls"] == 2
    assert fake_notion["sleeps"] == [1.0]


def test_long_retry_after_returns_immediately(fake_notion):
    fake_notion["responses"] = [(429, _error_body("rate_limited"), {"Retry-After": "30"})]
    with pytest.raises(NotionAPIError) as exc:
        notion_api.search_pages("anything")
    assert exc.value.to_dict()["retry_after_seconds"] == 30.0
    assert exc.value.retryable is True
    assert fake_notion["sleeps"] == []


def test_404_keeps_notion_message_and_hints_connections(fake_notion):
    fake_notion["responses"] = [
        (404, _error_body("object_not_found", "Could not find page with ID: abc."), {})
    ]
    with pytest.raises(NotionAPIError) as exc:
        notion_api.read_page(PAGE_ID)
    error = exc.value.to_dict()
    assert error["error"] == "object_not_found"
    assert error["message"] == "Could not find page with ID: abc."
    assert error["retryable"] is False
    assert "Connections" in error["hint"]
    assert fake_notion["calls"] == 1


def test_read_gives_up_after_max_retries(fake_notion):
    fake_notion["responses"] = [(503, _error_body("service_unavailable"), {})] * 4
    with pytest.raises(NotionAPIError) as exc:
        notion_api.search_pages("anything")
    assert exc.value.retryable is True
    assert fake_notion["calls"] == notion_api.MAX_RETRIES + 1
