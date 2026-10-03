# Week 2: Notion MCP Server

An MCP server (FastMCP, stdio transport) that lets a coding agent search, read, and append to Notion pages.

## Tools

| Tool | Type | What it does |
|---|---|---|
| `search_pages(query, limit=10)` | read | Find pages by title. Returns `page_id`, `title`, `url`, `last_edited`. |
| `read_page(page_id)` | read | Page content as Markdown, plus `title`, `url`, `truncated`. |
| `append_to_page(page_id, markdown)` | write | Append Markdown to the end of a page. Existing content is untouched. |

`page_id` for `read_page` and `append_to_page` comes from `search_pages`.

## Setup

1. Create an internal integration at https://www.notion.so/profile/integrations and copy its secret.
   It needs the read, update, and insert content capabilities.
2. In Notion, open the page(s) the agent may use: **••• → Connections → add your integration**.
   Child pages are shared automatically.
3. Create `week2/.env` (gitignored):
   ```
   NOTION_TOKEN=ntn_...
   ```
4. Install dependencies from the repo root, inside the Python environment you'll use
   (e.g. `conda activate cs146s`):
   ```
   poetry install
   ```

## Run

From the repo root, in that environment:

```
python week2/server.py
```

The server speaks MCP over stdin/stdout, so it waits silently for a client. To try the tools by hand:

```
fastmcp dev inspector week2/server.py
```

### Command for MCP clients

Clients like Claude Code launch the server themselves and don't activate conda, so give them the
environment's Python by absolute path:

```
/path/to/env/bin/python "/path/to/repo/week2/server.py"
```

For example: `/Users/<you>/miniconda3/envs/cs146s/bin/python`. The server finds `week2/.env` relative
to its own file, so it works from any working directory.
