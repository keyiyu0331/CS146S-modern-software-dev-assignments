"""Notion OAuth: interactive login (CLI only), token cache, and silent refresh.

Usage:
    python week2/auth.py login    # opens a browser once; saves tokens to week2/.notion_tokens.json
    python week2/auth.py status   # shows which workspace is connected (never prints tokens)
    python week2/auth.py logout   # revokes the token with Notion and deletes the cache

The MCP server only ever calls load_tokens() and refresh_tokens(). Neither opens a browser:
if the login can't be refreshed, the server returns an error asking the user to run `login`.
"""

import json
import os
import secrets
import sys
import threading
import time
import webbrowser
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlsplit

import httpx
from dotenv import load_dotenv

AUTHORIZE_URL = "https://api.notion.com/v1/oauth/authorize"
TOKEN_URL = "https://api.notion.com/v1/oauth/token"
REVOKE_URL = "https://api.notion.com/v1/oauth/revoke"

TOKEN_CACHE = Path(__file__).parent / ".notion_tokens.json"
LOGIN_TIMEOUT_SECONDS = 300

load_dotenv(Path(__file__).parent / ".env")

_refresh_lock = threading.Lock()


class AuthError(Exception):
    """The stored login is missing, expired, or revoked."""


def _redirect_uri() -> str:
    return os.environ.get("NOTION_REDIRECT_URI", "http://localhost:8765/callback")


def _client_credentials() -> tuple[str, str]:
    client_id = os.environ.get("NOTION_CLIENT_ID")
    client_secret = os.environ.get("NOTION_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise AuthError("NOTION_CLIENT_ID and NOTION_CLIENT_SECRET must be set in week2/.env.")
    return client_id, client_secret


# ---- Token cache ----


def load_tokens() -> dict[str, Any] | None:
    try:
        return json.loads(TOKEN_CACHE.read_text())
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def save_tokens(data: dict[str, Any]) -> None:
    data = {**data, "obtained_at": datetime.now(timezone.utc).isoformat()}
    data.pop("request_id", None)
    # Write to a temp file and rename, so a crash never leaves a half-written cache.
    tmp = TOKEN_CACHE.with_suffix(".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f, indent=2)
    os.chmod(tmp, 0o600)
    os.replace(tmp, TOKEN_CACHE)


# ---- Token endpoint ----


def _token_request(body: dict[str, Any]) -> dict[str, Any]:
    try:
        response = httpx.post(TOKEN_URL, auth=_client_credentials(), json=body, timeout=30.0)
    except httpx.HTTPError as e:
        raise AuthError(f"Could not reach Notion's token endpoint: {e}") from e
    if not response.is_success:
        try:
            detail = response.json().get("error") or response.json().get("code")
        except ValueError:
            detail = None
        raise AuthError(f"Notion rejected the token request ({response.status_code}, {detail}).")
    return response.json()


def exchange_code(code: str) -> dict[str, Any]:
    data = _token_request(
        {"grant_type": "authorization_code", "code": code, "redirect_uri": _redirect_uri()}
    )
    save_tokens(data)
    return data


def refresh_tokens(failed_access_token: str) -> str:
    """Get a new access token after `failed_access_token` was rejected. Returns the new token."""
    with _refresh_lock:
        cached = load_tokens()
        if not cached or not cached.get("refresh_token"):
            raise AuthError("No refresh token is stored.")
        # Another call may have refreshed while we waited for the lock. Refresh tokens rotate,
        # so refreshing again with the old one would fail.
        if cached.get("access_token") != failed_access_token:
            return cached["access_token"]

        data = _token_request(
            {"grant_type": "refresh_token", "refresh_token": cached["refresh_token"]}
        )
        if not data.get("refresh_token"):
            data["refresh_token"] = cached["refresh_token"]
        save_tokens({**cached, **data})
        return data["access_token"]


# ---- Interactive login (CLI only) ----


def _wait_for_callback(expected_state: str) -> str:
    """Serve one request on the redirect URI and return the authorization code."""
    redirect = urlsplit(_redirect_uri())
    result: dict[str, str] = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            url = urlsplit(self.path)
            if url.path != redirect.path:
                self.send_response(404)
                self.end_headers()
                return
            params = {k: v[0] for k, v in parse_qs(url.query).items()}
            if params.get("state") != expected_state:
                result["error"] = "state mismatch (possible CSRF); try logging in again"
            elif "error" in params:
                result["error"] = params["error"]
            elif "code" in params:
                result["code"] = params["code"]
            else:
                result["error"] = "no code in callback"
            ok = "code" in result
            self.send_response(200 if ok else 400)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            message = "Notion connected. You can close this tab." if ok else f"Login failed: {result['error']}"
            self.wfile.write(message.encode())

        def log_message(self, *args: Any) -> None:
            pass  # keep the terminal quiet

    server = HTTPServer((redirect.hostname or "localhost", redirect.port or 80), Handler)
    deadline = time.monotonic() + LOGIN_TIMEOUT_SECONDS
    try:
        # Keep serving until the callback arrives (ignoring stray requests like /favicon.ico).
        while not result:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            server.timeout = remaining
            server.handle_request()
    finally:
        server.server_close()

    if "code" not in result:
        raise AuthError(f"Login did not complete: {result.get('error', 'timed out')}.")
    return result["code"]


def login() -> dict[str, Any]:
    client_id, _ = _client_credentials()
    state = secrets.token_urlsafe(24)
    url = f"{AUTHORIZE_URL}?" + urlencode(
        {
            "client_id": client_id,
            "redirect_uri": _redirect_uri(),
            "response_type": "code",
            "owner": "user",
            "state": state,
        }
    )
    print("Opening Notion in your browser. If it doesn't open, visit:\n" + url)
    webbrowser.open(url)
    code = _wait_for_callback(state)
    return exchange_code(code)


def status() -> str:
    cached = load_tokens()
    if not cached:
        return "Not logged in. Run: python week2/auth.py login"
    return (
        f"Logged in to workspace {cached.get('workspace_name')!r} "
        f"(bot_id {cached.get('bot_id')}), tokens obtained {cached.get('obtained_at')}."
    )


def logout() -> str:
    cached = load_tokens()
    if not cached:
        return "Not logged in."
    try:
        httpx.post(
            REVOKE_URL,
            auth=_client_credentials(),
            json={"token": cached["access_token"]},
            timeout=30.0,
        )
    finally:
        TOKEN_CACHE.unlink(missing_ok=True)
    return "Revoked the token and deleted the local cache."


def main(argv: list[str]) -> int:
    command = argv[1] if len(argv) > 1 else ""
    try:
        if command == "login":
            data = login()
            print(f"Connected to workspace {data.get('workspace_name')!r}. Tokens saved to {TOKEN_CACHE}.")
        elif command == "status":
            print(status())
        elif command == "logout":
            print(logout())
        else:
            print(__doc__)
            return 2
    except AuthError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
