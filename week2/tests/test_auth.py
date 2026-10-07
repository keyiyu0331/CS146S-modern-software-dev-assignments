"""OAuth token cache, silent refresh on 401, and the mid-session expiry path. No network."""

import json
import stat

import httpx
import pytest

import auth
import notion_api
from notion_api import NotionAPIError

PAGE_ID = "3ec932b1-ff5f-8063-81bb-d15f413710fc"


@pytest.fixture
def oauth(monkeypatch, tmp_path):
    """Token cache in tmp_path, fake Notion API + token endpoint, and a browser that must not open."""
    monkeypatch.setattr(auth, "TOKEN_CACHE", tmp_path / "tokens.json")
    monkeypatch.setenv("NOTION_CLIENT_ID", "client-id")
    monkeypatch.setenv("NOTION_CLIENT_SECRET", "client-secret")
    monkeypatch.setattr(
        auth.webbrowser, "open", lambda *a, **k: pytest.fail("opened a browser during a tool call")
    )
    monkeypatch.setattr(notion_api.time, "sleep", lambda s: None)

    state = {"api": [], "api_calls": [], "token_responses": [], "token_calls": []}

    def fake_api(method, url, headers=None, **kwargs):
        state["api_calls"].append((method, headers["Authorization"]))
        status, body = state["api"].pop(0)
        return httpx.Response(status, json=body)

    def fake_token_post(url, auth=None, json=None, **kwargs):
        state["token_calls"].append(json)
        status, body = state["token_responses"].pop(0)
        return httpx.Response(status, json=body)

    monkeypatch.setattr(notion_api.httpx, "request", fake_api)
    monkeypatch.setattr(auth.httpx, "post", fake_token_post)
    return state


def _unauthorized():
    return (401, {"object": "error", "code": "unauthorized", "message": "API token is invalid."})


def test_401_refreshes_silently_and_saves_rotated_tokens(oauth):
    auth.save_tokens({"access_token": "old-access", "refresh_token": "old-refresh"})
    oauth["api"] = [_unauthorized(), (200, {"results": [], "has_more": False})]
    oauth["token_responses"] = [
        (200, {"access_token": "new-access", "refresh_token": "new-refresh", "token_type": "bearer"})
    ]

    assert notion_api.search_pages("x") == {"results": [], "has_more": False}

    assert oauth["token_calls"] == [{"grant_type": "refresh_token", "refresh_token": "old-refresh"}]
    assert [h for _, h in oauth["api_calls"]] == ["Bearer old-access", "Bearer new-access"]
    cached = auth.load_tokens()
    assert (cached["access_token"], cached["refresh_token"]) == ("new-access", "new-refresh")


def test_failed_refresh_returns_reauth_required_without_browser(oauth):
    auth.save_tokens({"access_token": "old-access", "refresh_token": "revoked"})
    oauth["api"] = [_unauthorized()]
    oauth["token_responses"] = [(400, {"error": "invalid_grant"})]

    with pytest.raises(NotionAPIError) as exc:
        notion_api.read_page(PAGE_ID)

    error = exc.value.to_dict()
    assert error["error"] == "reauth_required"
    assert error["retryable"] is False
    assert "auth.py login" in error["hint"]


def test_no_cached_login_returns_not_authenticated(oauth):
    with pytest.raises(NotionAPIError) as exc:
        notion_api.search_pages("x")
    assert exc.value.error == "not_authenticated"
    assert oauth["api_calls"] == []


def test_write_is_retried_once_after_refresh(oauth):
    auth.save_tokens({"access_token": "old-access", "refresh_token": "old-refresh"})
    oauth["api"] = [_unauthorized(), (200, {"id": PAGE_ID})]
    oauth["token_responses"] = [(200, {"access_token": "new-access", "refresh_token": "r2"})]

    result = notion_api.append_to_page(PAGE_ID, "hello")

    assert result["status"] == "appended"
    assert [m for m, _ in oauth["api_calls"]] == ["PATCH", "PATCH"]


def test_second_401_after_refresh_stops(oauth):
    auth.save_tokens({"access_token": "old-access", "refresh_token": "old-refresh"})
    oauth["api"] = [_unauthorized(), _unauthorized()]
    oauth["token_responses"] = [(200, {"access_token": "new-access", "refresh_token": "r2"})]

    with pytest.raises(NotionAPIError) as exc:
        notion_api.search_pages("x")
    assert exc.value.error == "reauth_required"
    assert len(oauth["token_calls"]) == 1


def test_null_refresh_token_keeps_previous_one(oauth):
    auth.save_tokens({"access_token": "old-access", "refresh_token": "keep-me"})
    oauth["token_responses"] = [(200, {"access_token": "new-access", "refresh_token": None})]

    assert auth.refresh_tokens("old-access") == "new-access"
    assert auth.load_tokens()["refresh_token"] == "keep-me"


def test_concurrent_refresh_reuses_newer_token(oauth):
    # Another call already refreshed: the cache no longer holds the token that failed.
    auth.save_tokens({"access_token": "already-new", "refresh_token": "r2"})
    assert auth.refresh_tokens("stale-access") == "already-new"
    assert oauth["token_calls"] == []


def test_cache_is_owner_only_and_status_hides_tokens(oauth):
    auth.save_tokens(
        {"access_token": "secret-a", "refresh_token": "secret-r", "workspace_name": "Test Workspace"}
    )
    mode = stat.S_IMODE(auth.TOKEN_CACHE.stat().st_mode)
    assert mode == 0o600
    assert "obtained_at" in json.loads(auth.TOKEN_CACHE.read_text())

    message = auth.status()
    assert "Test Workspace" in message
    assert "secret-a" not in message and "secret-r" not in message
