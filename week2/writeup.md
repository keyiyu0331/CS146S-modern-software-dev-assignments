# Week 2 Write-up

## Part I: The Server

**API chosen**, and why:
> **Notion.** I use it every day for course notes, so I could judge what the tools should do. The use
> case I designed for: "clean up my lecture notes": find a page, read it, and add an organized version.
> Notion supports OAuth 2.0 (public connections) with refresh tokens, and its API version `2026-03-11`
> has Markdown endpoints for reading and writing page content, which suit an agent much better than the
> nested block JSON (one paragraph is several levels of `type` / `paragraph` / `rich_text` objects).

**How to run it** (one command):
```
python week2/server.py
```
Run from the repo root in an environment with the dependencies installed (`poetry install`; I use
conda env `cs146s`). One-time setup is in `week2/README.md`: create a Notion public connection, fill
`week2/.env` from `.env.example`, and run `python week2/auth.py login`. MCP clients launch it with the
env's Python by absolute path (see `week2/.mcp.json.example`).

| Tool | What it does | Read/Write | Composes with |
|---|---|---|---|
| search_pages | Finds pages by title, most recently edited first. Returns `page_id`, `title`, `url`, `last_edited`, `parent_type`, `parent_id`, plus `has_more`. | Read | Its `page_id` feeds `read_page` and `append_to_page`; `parent_id` (when `parent_type` is `page`) feeds `read_page`. |
| read_page | Returns a page's content as Markdown, plus `title`, `url`, `truncated`. Accepts a page ID or a Notion URL. | Read | Takes `page_id` from `search_pages`; the `<page url="...">` links to child pages in its output can be passed straight back to `read_page`. |
| append_to_page | Appends Markdown to the end of a page without changing existing content. `dry_run=True` previews instead of writing. | Write | Takes `page_id` from `search_pages`; its Markdown is usually the agent's rewrite of `read_page` output. |


## Part II: Agent Ergonomics

For each, point at the code (`file:line`) and say what it buys.

| Decision | Where | Why |
|---|---|---|
| Schema-level constraint | `server.py:62`: `limit: Annotated[int, Field(ge=1, le=100)]` (Notion's `page_size` range) | The agent sees `minimum: 1, maximum: 100` *before* calling. A bad value like 500 is rejected by FastMCP without reaching Notion (`tests/test_tools.py:101`). Before, the schema said "any integer", so the agent only found out from a failed Notion call. The rule is stated once, in the schema, so prose and schema can't disagree. |
| Output shaping (fields kept vs. dropped) | `notion_api.py:214-327` (TypedDict outputs, `search_pages` shaping); `notion_api.py:330` (`read_page`) | Kept: what the agent needs to **choose** a page and **chain** to the next call (`page_id`, `title`, `url`, `last_edited`, `parent_type`/`parent_id`, `has_more`). Dropped: icons, covers, created/edited-by users, the nested `properties` structure, `request_id`. The title, buried at `properties → title → [ ] → plain_text`, is flattened to `title`. Writes return a short confirmation instead of the whole page Notion sends back. Raw search response for 2 pages: **2,015 chars** vs shaped: **567 chars** (3.6× smaller), measured on the same request as compact JSON. The gap grows with every result, since each page carries its own unused fields. The return types also become MCP **output schemas**, so the output contract is enforced too. |
| Structured errors (retry vs. don't-retry) | `notion_api.py:21` (`NotionAPIError`), `:58` (`HINTS`), `:145` (`_request`); converted to `ToolError` once in `server.py:48` | Every failure reaches the agent as `isError: true` with JSON `{error, message, retryable, hint}`. `message` is Notion's own explanation, which `raise_for_status()` used to discard. 400 (fix the input; get the ID from `search_pages`) and 404 (missing or not shared; ask the user to share it) get different hints. Retry policy: reads retry timeouts, network errors, 409, and 5xx up to 3 times with exponential backoff and jitter. Writes retry **only on 429**, because a timed-out write may already have been applied, and retrying would duplicate notes. Those errors instead say "may or may not have been applied, call read_page to check" (`notion_api.py:99`). A `Retry-After` over 5s is returned as `retry_after_seconds` rather than slept. |
| Docstring that chains tools together | `server.py:15` (`INSTRUCTIONS`), `:57-72` (`search_pages`), `:76-85` (`read_page`), `:32` (`PageIdParam`) | Docstrings say where each input comes from ("a page_id from search_pages, or a Notion page URL"), what to do when `has_more` is true, that `parent_id` can be read when `parent_type` is `page`, and that child-page links in `read_page` output can be passed back in. `INSTRUCTIONS` gives the cross-tool workflow (search → read → preview → append), says to ask the user when results are ambiguous, and says to retry only when `retryable` is true. |
| Brake on the write tool | `server.py:88-117` (`append_to_page`: annotations + `dry_run`), `notion_api.py:344` (`preview_append`) | `dry_run=True` writes nothing and returns the page title, the last 10 lines (`current_ending`), and `will_append`, so the user can confirm both the content and **where** it lands. Annotations: reads are `readOnlyHint: true`; the write is `destructiveHint: false` (it only adds) and `idempotentHint: false` (calling it twice adds twice). The default is `dry_run=False`; `INSTRUCTIONS` tells the agent to preview anything beyond a short addition and wait for the user's approval. In my transcript the agent did exactly that. Claude Code's per-tool permission prompt is a second, human brake. |

**One thing you changed after watching the agent misuse a tool:**
> No agent misused a tool during my testing; this change came from my own manual tests in the MCP Inspector. Calling `read_page` with a bad ID (`"a"`) returned FastMCP's default
> error: `Client error '400 Bad Request' for url '.../pages/a' For more information check:
> https://developer.mozilla.org/...`. From the model's point of view, it says nothing about what was
> wrong, how to fix it, or whether to retry, and Notion's useful message was discarded. I replaced it
> with structured errors. The same call now returns `validation_error` with Notion's message
> ("path.page_id should be a valid uuid, instead was "a"") and the hint "page_id must be an ID
> returned by search_pages." A well-formed but unknown ID returns `object_not_found` with a hint to
> share the page via Connections. I also tried `limit=500` the same way, which led to the schema
> constraint above.
>
> Considered and rejected: switching the write tool to *replace* page content, with a required
> preview-then-commit token to block stale approvals. I kept append because it can't lose the original
> notes, so a lighter brake (`dry_run`, plus guidance in the instructions) is proportionate.


## Part III: OAuth

**Flow**: how a token is obtained, cached, and refreshed:
> **Obtain** (`auth.py:177`, `python week2/auth.py login`, run by the user): generate a random `state`,
> open Notion's authorize URL (`response_type=code`, `owner=user`), and catch the redirect on a
> one-request local server at `http://localhost:8765/callback` (`auth.py:128`). The callback is
> rejected if `state` doesn't match (CSRF) or contains `error=access_denied`. The code is exchanged at
> `POST /v1/oauth/token` with HTTP Basic auth (client ID and secret).
> **Cache** (`auth.py:68`): the full token response is saved to `week2/.notion_tokens.json` with
> owner-only permissions (`600`), written to a temp file and renamed so it's never half-written. The
> server reads it on every request (`notion_api.py:104`), so logging in again takes effect without
> restarting the server.
> **Refresh** (`auth.py:105`, triggered at `notion_api.py:174`): Notion's token response has **no
> `expires_in`**, so the server can't refresh on a timer. Instead, when Notion returns **401**, it
> exchanges the refresh token, saves the new pair, and repeats the same request once. This is safe
> even for writes, because a 401 means Notion rejected the request without applying it. Refresh tokens
> **rotate**, so the new refresh token must be saved every time. A lock plus a "has someone already
> refreshed?" check stops two concurrent calls from both refreshing with the same (now invalid) token.
> Verified against the real API: I overwrote the cached access token with junk, and `read_page` still
> succeeded. Afterwards both the access and the refresh token had changed.

**Scopes requested**, and why each is necessary:
> Notion has no OAuth scope strings. Access is the public connection's **capabilities**, plus the
> **pages the user selects** on the consent screen, plus the installation scope ("Selected workspaces
> only": just my workspace).
> - **Read content**: `search_pages`, `read_page`.
> - **Insert content**: `append_to_page` adds new blocks.
> - **Update content**: also `append_to_page`, because Notion's Markdown PATCH endpoint requires the
>   update capability even for inserting.
> - **Not requested**: comments, and user information ("No user information"). No tool uses them.

**Secrets**: what's in env, what's gitignored:
> `week2/.env` (gitignored) holds `NOTION_CLIENT_ID` and `NOTION_CLIENT_SECRET`, read from the env by
> `auth.py`. Only `week2/.env.example`, with empty values, is committed. Gitignored as well: the token
> cache `.notion_tokens.json` (the rule was added before any code could write it) and the real
> `.mcp.json` (machine-specific paths). `.mcp.json` contains no secrets: the server finds `.env` and
> the cache relative to its own file. No token or secret was ever in code or in a commit. Development
> started with an internal-integration token, also only in `.env`, which was removed when OAuth
> replaced it.

**Token dies mid-session**: what the agent sees:
> The server **never opens a browser**. Only `login()` does, and only the CLI calls it, enforced by a
> test that fails if `webbrowser.open` is called (`tests/test_auth.py`). A browser opened inside a
> tool call would block the agent's turn for minutes, might appear on a machine nobody is watching, and
> its `print` of the URL would corrupt the stdio MCP stream. It would also let an agent trigger
> permission prompts on its own. Instead:
> - Access token rejected → silent refresh → the call succeeds; the agent never notices.
> - Refresh fails, or a second 401 after refreshing → `{"error": "reauth_required", "retryable": false,
>   "hint": "The Notion login expired or was revoked. Ask the user to run: python week2/auth.py login.
>   Do not retry until they have."}`
> - No login stored at all → `not_authenticated`, with the same hint.
>
> The agent asks the user to log in. Once they have, the same server process works on the next call.


## Part IV: Integration

**Registration config** (`.mcp.json.example`) and the client you used:
> Client: **Claude Code**. `week2/.mcp.json.example` is copied to `.mcp.json` at the repo root
> (gitignored), with absolute paths filled in:
> ```json
> {"mcpServers": {"notion": {"type": "stdio",
>   "command": "/path/to/your/env/bin/python",
>   "args": ["/path/to/modern-software-dev-assignments/week2/server.py"]}}}
> ```
> Absolute paths are needed because Claude Code starts the server itself and doesn't activate a conda
> env. After approving the project server, Claude Code received the server's `INSTRUCTIONS` and the
> three tools as `mcp__notion__search_pages` / `read_page` / `append_to_page`.

**End-to-end transcript**: the prompt, the tools that fired with their arguments, the result:
```
Prompt: "Can you clean up my CS146S lecture 1 notes in Notion and add an organized version at the bottom?"

1. search_pages(query="CS146S lecture 1")
   → {"results": [{"page_id": "3ef932b1-ff5f-80d3-a083-c0d69e492c6b", "title": "CS146S Lec1 Notes",
       "parent_type": "page", "parent_id": "3ec932b1-ff5f-8063-81bb-d15f413710fc",
       "last_edited": "2026-10-04T06:45:00.000Z", ...}], "has_more": false}

2. read_page(page_id="3ef932b1-ff5f-80d3-a083-c0d69e492c6b")
   → markdown: "we go over the method to building an code agent within 200 lines in this class
                1. coding agent\" is just an LLM in a loop:  2. **Tool registry** ... 8. **The agent loop**
                (`run_coding_agent_loop`  - A1 due sunday  - meet with group members ... branstorming",
     truncated: false

3. append_to_page(page_id=<same>, markdown="---\n## Lecture 1 — Organized Notes\n### Overview ...", dry_run=true)
   → {"dry_run": true, "title": "CS146S Lec1 Notes",
      "current_ending": "...- meet with group members to work on project proposal and branstorming",
      "will_append": "---\n## Lecture 1 — Organized Notes ..."}
   Agent showed the preview and what it changed (separated the overview from the components, moved
   the example tools into their own section, turned action items into to-dos, fixed typos), noted it
   did NOT invent explanations not in the notes, and asked to proceed.

User: "yes, write it to the page"

4. append_to_page(page_id=<same>, markdown=<same>)
   → {"page_id": "3ef932b1-...", "status": "appended", "characters_added": 539}

5. read_page(page_id=<same>)   (agent verified)
   → original notes unchanged; organized version appended after a divider with Overview /
     Components of the agent / Example tools / To-do (two Notion to-do blocks).
```

**A failure, handled**: what you provoked, what the agent saw, what it did next:
```
Provoked: in another terminal, `python week2/auth.py logout` (revokes the token, deletes the cache),
while Claude Code and the server kept running.

Prompt: "Read my CS146S lecture 1 notes"
read_page(page_id="3ef932b1-ff5f-80d3-a083-c0d69e492c6b")
→ isError: true
  {"error": "not_authenticated", "message": "No Notion login is stored.", "retryable": false,
   "hint": "Ask the user to run: python week2/auth.py login. Do not retry until they have."}

Agent: told the user it couldn't read the notes, asked them to run `python week2/auth.py login`,
and did not retry (retryable: false). No browser opened; the server kept running.

User ran login → "I just login again"
read_page(page_id=<same>) → succeeded, in the same server process (no restart).
```

**Protocol-level test**: what it covers and how to run it:
> `week2/tests/test_tools.py:101` and `:112` connect to the server with FastMCP's in-memory `Client`,
> so calls go through MCP `initialize` / `tools/list` / `tools/call` messages rather than calling
> Python functions directly. They check that `search_pages` with `limit=500` comes back as an MCP error
> without any Notion request being made, and that the agent-visible schemas carry `minimum`/`maximum`,
> the `dry_run` default, output schemas, and annotations (`readOnlyHint` on reads, `idempotentHint:
> false` on the write). The full suite (25 tests: errors and retries, ID parsing, shaping, `dry_run`,
> OAuth refresh and rotation, the no-browser guard) runs offline with faked HTTP:
> ```
> python -m pytest week2/tests
> ```
> During development I also drove the real server over **stdio**, launched with the exact command from
> `.mcp.json`, using FastMCP's `Client(StdioTransport(...))` against the live Notion API.


## Submission
1. `Command (⌘) + F` for `TODO`. No results means you're done.
2. Confirm no tokens, client secrets, cached token file, or real `.mcp.json` are committed.
3. Push all changes to your remote repository and submit via Gradescope.
4. Clean up (optional): remove the server from your agent config, delete your cached token, and revoke the OAuth app's access.
