"""Notion MCP server. Run with: python week2/server.py (stdio transport)."""

import json
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Annotated

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

import notion_api
from notion_api import AppendPreview, AppendResult, PageContent, SearchResult

INSTRUCTIONS = """\
Tools for reading and adding to the user's Notion pages. Only pages shared with this integration are visible.

Typical workflow:
1. search_pages to find the page and get its page_id. If several results look plausible, use
   last_edited and parent_type/parent_id to tell them apart, or ask the user which one they mean.
2. read_page to get the page content as Markdown.
3. append_to_page to add content at the end of the page. Existing content is never changed.
   For anything beyond a short addition, first call it with dry_run=True, show the user the
   preview, and only write after they agree.

If the user gives a Notion link, pass it directly as page_id; no search is needed.
Errors are JSON with error, message, retryable, and hint. Follow the hint, and only retry when
retryable is true (after retry_after_seconds, if given)."""

mcp = FastMCP("notion", instructions=INSTRUCTIONS)

PageIdParam = Annotated[
    str,
    Field(
        description="A page_id from search_pages, or a Notion page URL (the ID is extracted from it)."
    ),
]

READ_ONLY = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": True,
}


@contextmanager
def notion_errors() -> Iterator[None]:
    """Turn NotionAPIError into a ToolError (isError: true) whose message is the error dict as JSON."""
    try:
        yield
    except notion_api.NotionAPIError as e:
        raise ToolError(json.dumps(e.to_dict())) from e


@mcp.tool(annotations=READ_ONLY)
def search_pages(
    query: Annotated[
        str,
        Field(description="Words to match in page titles. Use an empty string to list recent pages."),
    ],
    limit: Annotated[int, Field(ge=1, le=100, description="Maximum number of results.")] = 10,
) -> SearchResult:
    """Find Notion pages by title, most recently edited first.

    Matches page titles only, not page content. Each result's page_id can be passed to read_page
    or append_to_page. If parent_type is "page", parent_id can be passed to read_page to see the
    parent page. If has_more is true, more pages matched than were returned: narrow the query or
    raise limit.
    """
    with notion_errors():
        return notion_api.search_pages(query, limit)


@mcp.tool(annotations=READ_ONLY)
def read_page(page_id: PageIdParam) -> PageContent:
    """Read a Notion page's content as Markdown.

    Headings, lists, and to-dos keep their Markdown structure. Child pages appear as
    <page url="...">title</page>; pass that url as page_id to read the child page. Media and
    unsupported blocks appear as tags or <unknown .../>. If truncated is true, part of the page
    could not be loaded, so do not treat the content as complete.
    """
    with notion_errors():
        return notion_api.read_page(page_id)


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
def append_to_page(
    page_id: PageIdParam,
    markdown: Annotated[
        str,
        Field(
            description="Markdown to add at the end of the page: headings (#), bullets (-), "
            "numbered lists (1.), to-dos (- [ ]), and paragraphs become Notion blocks."
        ),
    ],
    dry_run: Annotated[
        bool,
        Field(description="If true, write nothing and return a preview of where the content would go."),
    ] = False,
) -> AppendResult | AppendPreview:
    """Add Markdown content to the end of a Notion page. Existing content is left unchanged.

    This writes to the user's real page, and calling it twice adds the content twice. With
    dry_run=true it returns the page title, the last lines of the page (current_ending), and the
    content that would be appended (will_append), without writing anything.
    """
    with notion_errors():
        return notion_api.append_to_page(page_id, markdown, dry_run)


if __name__ == "__main__":
    mcp.run()
