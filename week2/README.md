# Week 2: Notion MCP Server

An MCP server (FastMCP, stdio transport) that lets a coding agent search, read, and append to Notion pages.

## Tools

| Tool | Type | What it does |
|---|---|---|
| `search_pages(query, limit=10)` | read | Find pages by title (`limit` 1–100). Returns `results` (`page_id`, `title`, `url`, `last_edited`, `parent_type`, `parent_id`) and `has_more`. |
| `read_page(page_id)` | read | Page content as Markdown, plus `title`, `url`, `truncated`. |
| `append_to_page(page_id, markdown, dry_run=False)` | write | Append Markdown to the end of a page; existing content is untouched. `dry_run=True` previews the page's current ending and the new content without writing. |

`page_id` for `read_page` and `append_to_page` comes from `search_pages`, or can be a Notion page URL.

Errors are returned as MCP tool errors whose text is JSON: `error`, `message`, `retryable`, `hint`
(and `retry_after_seconds` when rate limited). Reads retry transient failures up to 3 times; writes
only retry on rate limits, so a failed write never duplicates content.

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

## Tests

```
python -m pytest week2/tests
```

No network or token needed: Notion's HTTP responses are faked. Some tests call the server through an
in-memory MCP client.
