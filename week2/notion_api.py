"""Plain Python wrappers around the Notion API. No MCP code lives here."""

import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2026-03-11"


def get_token() -> str:
    """Return the Notion token. The only place the token is read (swapped for OAuth in Part III)."""
    # Resolve .env relative to this file: the MCP client may launch us from any working directory.
    load_dotenv(Path(__file__).parent / ".env")
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise RuntimeError("NOTION_TOKEN is not set. Add it to week2/.env.")
    return token


def _request(method: str, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
    response = httpx.request(
        method,
        f"{NOTION_API_URL}{path}",
        headers={
            "Authorization": f"Bearer {get_token()}",
            "Notion-Version": NOTION_VERSION,
        },
        json=json,
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


def _extract_title(page: dict[str, Any]) -> str:
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            title = "".join(part.get("plain_text", "") for part in prop.get("title", []))
            return title or "(untitled)"
    return "(untitled)"


def search_pages(query: str, limit: int = 10) -> list[dict[str, Any]]:
    data = _request(
        "POST",
        "/search",
        json={
            "query": query,
            "filter": {"property": "object", "value": "page"},
            "sort": {"direction": "descending", "timestamp": "last_edited_time"},
            "page_size": limit,
        },
    )
    return [
        {
            "page_id": page["id"],
            "title": _extract_title(page),
            "url": page.get("url"),
            "last_edited": page.get("last_edited_time"),
        }
        for page in data.get("results", [])
    ]
