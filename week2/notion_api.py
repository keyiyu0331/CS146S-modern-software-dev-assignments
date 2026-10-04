"""Plain Python wrappers around the Notion API. No MCP code lives here."""

import random
import re
import time
from typing import Any, Literal, TypedDict
from urllib.parse import urlsplit

import httpx

import auth

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2026-03-11"

MAX_RETRIES = 3
MAX_SLEEP_SECONDS = 5.0
PREVIEW_LINES = 10


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
_LOGIN_HINT = (
    "The Notion login expired or was revoked. Ask the user to run: python week2/auth.py login. "
    "Do not retry until they have."
)

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
    "unauthorized": (False, _LOGIN_HINT),
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
    """Return the cached OAuth access token. Never starts a login (that needs a browser)."""
    tokens = auth.load_tokens()
    if not tokens or not tokens.get("access_token"):
        raise NotionAPIError(
            "not_authenticated",
            "No Notion login is stored.",
            retryable=False,
            hint="Ask the user to run: python week2/auth.py login. Do not retry until they have.",
        )
    return tokens["access_token"]


def _reauth_required(message: str) -> NotionAPIError:
    return NotionAPIError("reauth_required", message, retryable=False, hint=_LOGIN_HINT)


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
    """Call Notion, refreshing an expired login once and retrying transient failures.

    retry_safe: whether repeating the call can't cause duplicate effects. Reads pass True;
    writes pass False and are only retried on 429 (Notion rejected them without applying).
    A 401 is retried for writes too, after a token refresh: Notion rejected it unapplied.
    """
    token = get_token()
    refreshed = False
    attempt = 0

    while True:
        headers = {"Authorization": f"Bearer {token}", "Notion-Version": NOTION_VERSION}
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

            if response.status_code == 401:
                if refreshed:
                    raise _reauth_required("Notion rejected the token even after refreshing it.")
                try:
                    token = auth.refresh_tokens(token)
                except auth.AuthError as e:
                    raise _reauth_required(str(e)) from e
                refreshed = True
                continue  # same request with the new token; doesn't count as a retry

            error = _error_from_response(response)
            uncertain_write = response.status_code >= 500

            if response.status_code == 429:
                wait = _retry_after(response)
                error.retry_after_seconds = wait
                # A long wait is better spent by the agent than by blocking here.
                if wait > MAX_SLEEP_SECONDS or attempt == MAX_RETRIES:
                    raise error
                time.sleep(wait)
                attempt += 1
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
        attempt += 1


# ---- Output shapes (FastMCP turns these into each tool's output schema) ----

ParentType = Literal["workspace", "page", "database", "block"]


class PageHit(TypedDict):
    page_id: str
    title: str
    url: str | None
    last_edited: str | None
    parent_type: ParentType
    parent_id: str | None


class SearchResult(TypedDict):
    results: list[PageHit]
    has_more: bool


class PageContent(TypedDict):
    page_id: str
    title: str
    url: str | None
    markdown: str
    truncated: bool


class AppendResult(TypedDict):
    page_id: str
    status: Literal["appended"]
    characters_added: int


class AppendPreview(TypedDict):
    dry_run: Literal[True]
    page_id: str
    title: str
    current_ending: str
    will_append: str


# ---- Helpers ----

# A dashed UUID or 32 hex chars at the end of the string (Notion URLs end in the undashed ID).
_PAGE_ID_RE = re.compile(
    r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|[0-9a-f]{32})$", re.IGNORECASE
)

# Notion parent.type -> our parent_type
_PARENT_TYPES: dict[str, ParentType] = {
    "workspace": "workspace",
    "page_id": "page",
    "database_id": "database",
    "data_source_id": "database",
    "block_id": "block",
}


def normalize_page_id(value: str) -> str:
    """Accept a page ID (dashed or not) or a Notion page URL; return the dashed ID."""
    text = value.strip()
    path = urlsplit(text).path if "://" in text else text
    match = _PAGE_ID_RE.search(path.rstrip("/"))
    if not match:
        raise NotionAPIError(
            "validation_error",
            f"Could not find a Notion page ID in {value!r}.",
            retryable=False,
            hint="Pass a page_id from search_pages or a Notion page URL.",
        )
    raw = match.group(1).replace("-", "").lower()
    return f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"


def _extract_title(page: dict[str, Any]) -> str:
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            title = "".join(part.get("plain_text", "") for part in prop.get("title", []))
            return title or "(untitled)"
    return "(untitled)"


def _parent(page: dict[str, Any]) -> tuple[ParentType, str | None]:
    parent = page.get("parent", {})
    kind = parent.get("type", "workspace")
    parent_type = _PARENT_TYPES.get(kind, "block")
    parent_id = None if kind == "workspace" else parent.get(kind)
    return parent_type, parent_id


# ---- Operations ----


def search_pages(query: str, limit: int = 10) -> SearchResult:
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
    results: list[PageHit] = []
    for page in data.get("results", []):
        parent_type, parent_id = _parent(page)
        results.append(
            {
                "page_id": page["id"],
                "title": _extract_title(page),
                "url": page.get("url"),
                "last_edited": page.get("last_edited_time"),
                "parent_type": parent_type,
                "parent_id": parent_id,
            }
        )
    return {"results": results, "has_more": bool(data.get("has_more", False))}


def read_page(page_id: str) -> PageContent:
    page_id = normalize_page_id(page_id)
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


def preview_append(page_id: str, markdown: str) -> AppendPreview:
    """Show where `markdown` would land without writing anything."""
    page = read_page(page_id)
    ending = "\n".join(page["markdown"].splitlines()[-PREVIEW_LINES:])
    return {
        "dry_run": True,
        "page_id": page["page_id"],
        "title": page["title"],
        "current_ending": ending,
        "will_append": markdown,
    }


def append_to_page(
    page_id: str, markdown: str, dry_run: bool = False
) -> AppendResult | AppendPreview:
    if dry_run:
        return preview_append(page_id, markdown)
    page_id = normalize_page_id(page_id)
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
