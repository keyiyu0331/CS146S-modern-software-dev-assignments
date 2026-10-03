"""Notion MCP server. Run with: python week2/server.py (stdio transport)."""

from typing import Any

from fastmcp import FastMCP

import notion_api

mcp = FastMCP("notion")


@mcp.tool
def search_pages(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Search Notion pages shared with this integration by title. Returns page_id, title, url, last_edited."""
    return notion_api.search_pages(query, limit)


@mcp.tool
def read_page(page_id: str) -> dict[str, Any]:
    """Read a Notion page's content as Markdown. page_id comes from search_pages.
    Returns page_id, title, url, markdown, truncated."""
    return notion_api.read_page(page_id)


if __name__ == "__main__":
    mcp.run()
