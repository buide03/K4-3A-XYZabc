from __future__ import annotations

import argparse
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
ARTIFACTS_DIR = ROOT / "artifacts"

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools

load_lab_env(ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke-test live structured tool calling.")
    parser.add_argument("--provider", choices=["openrouter", "openai", "gemini", "groq"], default="openrouter")
    parser.add_argument("--model", default=None, help="Optional model override. Omit to use provider default from code.")
    parser.add_argument("--tools", type=Path, default=ARTIFACTS_DIR / "tools.yaml")
    args = parser.parse_args()

    provider = make_provider(args.provider)
    tools = to_openai_tools(load_tool_declarations(args.tools))
    messages = [
        {"role": "system", "content": "You are a tool-routing smoke test. Use tools when appropriate."},
        {"role": "user", "content": "Hôm nay tôi xin nghỉ ốm, bot sửa điểm danh giúp tôi được không?"},
    ]
    response = provider.complete(messages, tools, model=args.model, temperature=0.0)
    selected_model = args.model or getattr(provider, "default_model", None)
    print(f"OK provider={args.provider} model={selected_model}")
    print(f"text={response.text}")
    if response.tool_calls:
        first = response.tool_calls[0]
        print(f"tool={first.name}")
        print(f"args={first.args}")


if __name__ == "__main__":
    main()

