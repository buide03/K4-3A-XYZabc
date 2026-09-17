from __future__ import annotations

import sys
from pathlib import Path

CODEBASE_DIR = Path(__file__).resolve().parent.parent / "codebase"
if str(CODEBASE_DIR) not in sys.path:
    sys.path.insert(0, str(CODEBASE_DIR))

from codebase.providers.base_provider import BaseProvider
from codebase.providers.openai_provider import OpenAIProvider
from codebase.providers.openrouter_provider import OpenRouterProvider
from codebase.providers.gemini_provider import GeminiProvider
from codebase.providers.groq_provider import GroqProvider
from codebase.providers.anthropic_provider import AnthropicProvider
from codebase.providers import get_provider, make_provider

__all__ = [
    "BaseProvider",
    "OpenAIProvider",
    "OpenRouterProvider",
    "GeminiProvider",
    "GroqProvider",
    "AnthropicProvider",
    "get_provider",
    "make_provider",
]
