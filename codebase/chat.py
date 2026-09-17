from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from env_loader import load_lab_env
from providers import make_provider
from providers.base import ToolCall
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
load_lab_env(ROOT)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def execute_tool_call(call: ToolCall) -> dict[str, Any]:
    func = TOOL_FUNCTIONS.get(call.name)
    if not func:
        return {
            "tool": call.name,
            "args": call.args,
            "result": {"error": "unknown_tool", "message": f"Không tìm thấy tool {call.name}"},
        }
    try:
        result = func(**call.args)
    except Exception as exc:
        result = {"error": type(exc).__name__, "message": str(exc)}
    return {"tool": call.name, "args": call.args, "result": result}


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI Chat tương tác với Trợ lý Quy chế Khóa 4.")
    parser.add_argument("--provider", default="openrouter", choices=["openrouter", "openai", "gemini", "groq"])
    parser.add_argument("--model", default=None, help="Mô hình LLM (mặc định openai/gpt-4o-mini cho openrouter)")
    parser.add_argument("--version", default="v0", help="Phiên bản prompt (v0, v1)")
    args = parser.parse_args()

    provider = make_provider(args.provider)
    model_name = args.model or getattr(provider, "default_model", "openai/gpt-4o-mini")

    prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"
    system_prompt = prompt_path.read_text(encoding="utf-8") if prompt_path.is_file() else ""
    tools = to_openai_tools(load_tool_declarations(tools_path))

    version_info = build_artifact_version(args.version, prompt_path, tools_path)

    print("================================================================")
    print(" 🤖 TRỢ LÝ QUY CHẾ & LỊCH NỘP BÀI KHÓA 4 — CLI CHAT")
    print(f" Provider: {args.provider.upper()} | Model: {model_name}")
    print(f" Version: {version_info.artifact_version}")
    print(" Gõ 'exit' hoặc 'quit' để thoát.")
    print("================================================================\n")

    history: list[dict[str, str]] = []
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript_file = TRANSCRIPTS_DIR / f"chat_{session_id}.json"

    while True:
        try:
            user_input = input("\n[Học viên]: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Tạm biệt học viên!")
                break

            history.append({"role": "user", "content": user_input})
            messages = [{"role": "system", "content": system_prompt}, *history]

            response = provider.complete(messages, tools, model=model_name, temperature=0.1)

            # Xử lý nếu mô hình gọi tool
            if response.tool_calls:
                for call in response.tool_calls:
                    print(f"⚙️  [Tool Call]: {call.name}({call.args})")
                    tool_res = execute_tool_call(call)
                    print(f"   [Tool Result]: {tool_res['result']}")

            reply_text = response.text or ""
            if not reply_text and response.tool_calls:
                reply_text = f"Đã thực hiện công cụ {response.tool_calls[0].name}."

            print(f"\n[Trợ lý]: {reply_text}")
            history.append({"role": "assistant", "content": reply_text})

            # Ghi transcript
            with open(transcript_file, "w", encoding="utf-8") as f:
                json.dump({
                    "session_id": session_id,
                    "provider": args.provider,
                    "model": model_name,
                    "version": artifact_version_dict(version_info),
                    "history": history
                }, f, ensure_ascii=False, indent=2)

        except KeyboardInterrupt:
            print("\nĐã dừng phiên chat.")
            break
        except Exception as e:
            print(f"\n❌ Lỗi: {e}")


if __name__ == "__main__":
    main()

