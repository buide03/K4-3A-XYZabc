from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml

from .clarify.tool import ask_user
from .create_ticket.tool import create_ticket
from .search_policy.tool import search_policy

TOOL_FUNCTIONS = {
    "clarify": ask_user,
    "create_ticket": create_ticket,
    "search_policy": search_policy,
}


def load_tool_declarations(path: Path) -> list[dict[str, Any]]:
    if not Path(path).is_file():
        return []
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")).get("tools", [])


def to_openai_tools(declarations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{
        "type": "function",
        "function": {
            "name": item["name"],
            "description": item.get("description", ""),
            "parameters": item.get("parameters", {"type": "object", "properties": {}}),
        },
    } for item in declarations]


__all__ = [
    "TOOL_FUNCTIONS",
    "load_tool_declarations",
    "to_openai_tools",
]

