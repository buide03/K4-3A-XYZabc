from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from env_loader import load_lab_env
from providers import make_provider, get_provider

ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
PORT = int(os.getenv("PORT", "8000"))
load_lab_env(ROOT)


class ChatAppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")

            try:
                body = json.loads(post_data)
                user_message = body.get("message", "").strip()
                if not user_message:
                    self._send_json({"error": "Tin nhắn rỗng"}, status=400)
                    return

                provider = get_provider()
                model_name = getattr(provider, "default_model", "openai/gpt-4o-mini")

                prompt_path = ARTIFACTS_DIR / "system_prompt.md"
                system_prompt = prompt_path.read_text(encoding="utf-8") if prompt_path.is_file() else ""

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ]

                response = provider.complete(messages, tools=None, model=model_name, temperature=0.1)
                reply = response.text or ""

                # Ghi vết logging phục vụ xác minh kỹ thuật
                transcripts_dir = ROOT / "transcripts"
                transcripts_dir.mkdir(parents=True, exist_ok=True)
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "provider": provider.__class__.__name__,
                    "model": model_name,
                    "prompt_input": messages,
                    "raw_response": getattr(response, "raw_payload", None) or {"text": reply},
                    "reply_text": reply
                }
                try:
                    with open(transcripts_dir / "app_chat_transcripts.jsonl", "a", encoding="utf-8") as lf:
                        lf.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
                except Exception:
                    pass

                self._send_json({
                    "reply": reply,
                    "provider": provider.__class__.__name__,
                    "model": model_name,
                    "status": "success"
                })
            except Exception as e:
                provider = get_provider()
                self._send_json({
                    "error": str(e),
                    "provider": provider.__class__.__name__,
                    "status": "error"
                }, status=500)
        else:
            self._send_json({"error": "Endpoint không tồn tại"}, status=404)

    def _send_json(self, data, status=200):
        response_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run():
    load_lab_env(ROOT)
    provider = get_provider()
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, ChatAppHandler)
    print(f"============================================================")
    print(f" Mini Hackathon AI B04 — CP3 Core Engine Running")
    print(f" Provider: {provider.__class__.__name__} | Model: {provider.default_model}")
    print(f" Mở trình duyệt tại: http://localhost:{PORT}")
    print(f" Gõ câu hỏi để test thật và quay video 30 giây")
    print(f" Nhấn Ctrl + C để dừng server")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng server an toàn.")


if __name__ == "__main__":
    run()
