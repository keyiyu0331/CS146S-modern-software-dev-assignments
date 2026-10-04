import sys
from pathlib import Path

import pytest

# Make week2/ importable (notion_api, server) without packaging it.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def anyio_backend():
    # Run async (MCP client) tests on asyncio only; trio isn't installed.
    return "asyncio"
