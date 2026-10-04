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

The server authenticates with OAuth 2.0 (authorization-code flow) through a Notion **public connection**.

1. In the Notion Developer portal (https://app.notion.com/developers/connections), go to
   **Public connections → Create new connection**:
   - Redirect URI: `http://localhost:8765/callback`
   - Installation scope: **Selected workspaces only** (your workspace)
   - Capabilities: **Read content**, **Update content**, **Insert content**; no comments, no user information.
     Read is used by `search_pages`/`read_page`; update + insert by `append_to_page`.
2. Copy `week2/.env.example` to `week2/.env` (gitignored) and fill in the **OAuth client ID** and
   **client secret** from the connection's Configuration tab.
3. Install dependencies from the repo root, inside the Python environment you'll use
   (e.g. `conda activate cs146s`):
   ```
   poetry install
   ```
4. Log in once. This opens Notion's consent screen in your browser; pick the pages the agent may use:
   ```
   python week2/auth.py login
   ```
   Tokens are saved to `week2/.notion_tokens.json` (gitignored, owner-only permissions).
   `python week2/auth.py status` shows the connected workspace; `python week2/auth.py logout` revokes
   the token and deletes the cache.

The server never opens a browser. When Notion rejects the access token (401), it refreshes it with the
refresh token, saves the new pair (refresh tokens rotate), and retries the request once. If refreshing
fails, tools return a `reauth_required` error telling the user to run `login` again.

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
