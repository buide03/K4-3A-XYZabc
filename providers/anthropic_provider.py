from __future__ import annotations

import sys
from pathlib import Path

CODEBASE_DIR = Path(__file__).resolve().parent.parent / "codebase"
if str(CODEBASE_DIR) not in sys.path:
    sys.path.insert(0, str(CODEBASE_DIR))

from codebase.providers.anthropic_provider import AnthropicProvider

__all__ = ["AnthropicProvider"]

