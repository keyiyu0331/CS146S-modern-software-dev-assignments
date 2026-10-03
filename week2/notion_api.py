"""Plain Python wrappers around the Notion API. No MCP code lives here."""

import os
import random
import time
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2026-03-11"

MAX_RETRIES = 3
MAX_SLEEP_SECONDS = 5.0


class NotionAPIError(Exception):
    """A Notion failure described as data the agent can act on."""

    def __init__(
        self,
        error: str,
        message: str,
        retryable: bool,
        hint: str,
        retry_after_seconds: float | None = None,
    ) -> None:
        super().__init__(message)
        self.error = error
        self.message = message
        self.retryable = retryable
        self.hint = hint
        self.retry_after_seconds = retry_after_seconds

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "error": self.error,
            "message": self.message,
            "retryable": self.retryable,
            "hint": self.hint,
        }
        if self.retry_after_seconds is not None:
            result["retry_after_seconds"] = self.retry_after_seconds
        return result


_TRANSIENT_HINT = "Notion is temporarily unavailable. Retry shortly."

# Keyed by Notion's error `code`: (retryable, hint).
HINTS: dict[str, tuple[bool, str]] = {
    "validation_error": (
        False,
        "Check the arguments. page_id must be an ID returned by search_pages.",
    ),
    "object_not_found": (
        False,
        "The page does not exist or is not shared with this integration. Use search_pages to find "
        "it, or ask the user to share it via the page's ••• menu → Connections.",
    ),
    "unauthorized": (
        False,
        "The Notion token is invalid or revoked. Ask the user to update NOTION_TOKEN.",
    ),
    "restricted_resource": (
        False,
        "The integration lacks a required capability. Ask the user to enable it in the "
        "integration's Capabilities settings.",
    ),
    "rate_limited": (True, "Wait retry_after_seconds, then retry."),
    "conflict_error": (True, _TRANSIENT_HINT),
    "internal_server_error": (True, _TRANSIENT_HINT),
    "bad_gateway": (True, _TRANSIENT_HINT),
    "service_unavailable": (True, _TRANSIENT_HINT),
    "gateway_timeout": (True, _TRANSIENT_HINT),
    "timeout": (True, _TRANSIENT_HINT),
    "network_error": (True, _TRANSIENT_HINT),
}

# Fallback when the error body isn't Notion's JSON.
_STATUS_CODES = {
    400: "validation_error",
    401: "unauthorized",
    403: "restricted_resource",
    404: "object_not_found",
    409: "conflict_error",
    429: "rate_limited",
    500: "internal_server_error",
    502: "bad_gateway",
    503: "service_unavailable",
    504: "gateway_timeout",
}

# A write that timed out or hit a server error may already have been applied.
_WRITE_UNCERTAIN_HINT = (
    "The append may or may not have been applied. Call read_page to check before retrying."
)


def get_token() -> str:
    """Return the Notion token. The only place the token is read (swapped for OAuth in Part III)."""
    # Resolve .env relative to this file: the MCP client may launch us from any working directory.
    load_dotenv(Path(__file__).parent / ".env")
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise NotionAPIError(
            "not_configured",
            "NOTION_TOKEN is not set.",
            retryable=False,
            hint="Ask the user to add NOTION_TOKEN to week2/.env and restart the server.",
        )
    return token


def _error_from(code: str, message: str) -> NotionAPIError:
    retryable, hint = HINTS.get(code, (False, "Unexpected Notion error."))
    return NotionAPIError(code, message, retryable, hint)


def _error_from_response(response: httpx.Response) -> NotionAPIError:
    try:
        body = response.json()
    except ValueError:
        body = {}
    code = body.get("code") or _STATUS_CODES.get(response.status_code, "unexpected_error")
    error = _error_from(code, body.get("message") or f"HTTP {response.status_code}")
    if response.status_code >= 500 and code not in HINTS:
        error.retryable, error.hint = True, _TRANSIENT_HINT
    return error


def _retry_after(response: httpx.Response) -> float:
    try:
        return float(response.headers.get("Retry-After", "1"))
    except ValueError:
        return 1.0


def _request(
    method: str, path: str, json: dict[str, Any] | None = None, *, retry_safe: bool
) -> dict[str, Any]:
    """Call Notion, retrying transient failures.

    retry_safe: whether repeating the call can't cause duplicate effects. Reads pass True;
    writes pass False and are only retried on 429 (Notion rejected them without applying).
    """
    headers = {"Authorization": f"Bearer {get_token()}", "Notion-Version": NOTION_VERSION}

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = httpx.request(
                method, f"{NOTION_API_URL}{path}", headers=headers, json=json, timeout=30.0
            )
        except httpx.TimeoutException:
            error = _error_from("timeout", "Request to Notion timed out.")
            uncertain_write = True
        except httpx.TransportError as e:
            error = _error_from("network_error", f"Could not reach Notion: {e}")
            uncertain_write = True
        else:
            if response.is_success:
                return response.json()
            error = _error_from_response(response)
            uncertain_write = response.status_code >= 500

            if response.status_code == 429:
                wait = _retry_after(response)
                error.retry_after_seconds = wait
                # A long wait is better spent by the agent than by blocking here.
                if wait > MAX_SLEEP_SECONDS or attempt == MAX_RETRIES:
                    raise error
                time.sleep(wait)
                continue

        if not error.retryable:
            raise error
        if not retry_safe:
            if uncertain_write:
                error.hint = _WRITE_UNCERTAIN_HINT
            raise error
        if attempt == MAX_RETRIES:
            raise error
        time.sleep(0.5 * 2**attempt + random.uniform(0, 0.25))

    raise AssertionError("unreachable")


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
        retry_safe=True,
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


def read_page(page_id: str) -> dict[str, Any]:
    # The markdown endpoint doesn't include the title, so fetch the page object too.
    page = _request("GET", f"/pages/{page_id}", retry_safe=True)
    content = _request("GET", f"/pages/{page_id}/markdown", retry_safe=True)
    return {
        "page_id": page["id"],
        "title": _extract_title(page),
        "url": page.get("url"),
        "markdown": content.get("markdown", ""),
        "truncated": content.get("truncated", False),
    }


def append_to_page(page_id: str, markdown: str) -> dict[str, Any]:
    # insert_content is marked deprecated by Notion, but it is the only markdown command that
    # appends without rewriting existing content. Pinned NOTION_VERSION keeps it stable.
    result = _request(
        "PATCH",
        f"/pages/{page_id}/markdown",
        json={
            "type": "insert_content",
            "insert_content": {"content": markdown, "position": {"type": "end"}},
        },
        retry_safe=False,
    )
    # Notion returns the whole page as markdown; return a short confirmation instead.
    return {
        "page_id": result.get("id", page_id),
        "status": "appended",
        "characters_added": len(markdown),
    }
