import sys
from pathlib import Path

# Make week2/ importable (notion_api, server) without packaging it.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
