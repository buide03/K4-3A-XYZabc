from __future__ import annotations

import os
from providers.openai_provider import OpenAIProvider
from providers.openrouter_provider import OpenRouterProvider
from providers.gemini_provider import GeminiProvider
from providers.groq_provider import GroqProvider
from providers.anthropic_provider import AnthropicProvider


def make_provider(name: str):
    name = (name or "").lower().strip()
    if name == "openai":
        return OpenAIProvider()
    if name == "openrouter":
        return OpenRouterProvider()
    if name == "gemini":
        return GeminiProvider()
    if name == "groq":
        return GroqProvider()
    if name == "anthropic":
        return AnthropicProvider()
    raise ValueError(f"Unknown provider: {name}")


def get_provider(name: str | None = None):
    provider_name = name or os.getenv("LLM_PROVIDER", "openrouter")
    return make_provider(provider_name)


__all__ = [
    "OpenAIProvider",
    "OpenRouterProvider",
    "GeminiProvider",
    "GroqProvider",
    "AnthropicProvider",
    "make_provider",
    "get_provider",
]
