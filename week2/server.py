"""Notion MCP server. Run with: python week2/server.py (stdio transport)."""

from typing import Any

from fastmcp import FastMCP

import notion_api

mcp = FastMCP("notion")


@mcp.tool
def search_pages(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Search Notion pages shared with this integration by title. Returns page_id, title, url, last_edited."""
    return notion_api.search_pages(query, limit)


if __name__ == "__main__":
    mcp.run()
