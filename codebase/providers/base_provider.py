from __future__ import annotations

import os
import json
import time
from abc import ABC, abstractmethod
from pathlib import Path
from dotenv import load_dotenv

# Tự động nạp .env
load_dotenv()

# Đường dẫn ghi log xác minh kỹ thuật cho CP3
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
TRACE_LOG_FILE = LOG_DIR / "llm_trace.jsonl"


class BaseProvider(ABC):
    """Lớp trừu tượng định nghĩa giao diện chung cho mọi LLM Provider."""

    def __init__(
        self,
        api_key_env: str,
        default_model: str,
        base_url: str | None = None,
    ) -> None:
        self.api_key_env = api_key_env
        self.api_key = os.getenv(api_key_env, "").strip()
        self.default_model = default_model
        self.base_url = base_url
        self.temperature = float(os.getenv("TEMPERATURE", "0.1"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000"))

    def get_api_key(self) -> str:
        key = os.getenv(self.api_key_env, self.api_key).strip()
        if not key or key.startswith("your_"):
            raise ValueError(
                f"Chưa cấu hình API Key trong biến môi trường '{self.api_key_env}'. "
                f"Vui lòng điền API key vào tệp .env."
            )
        return key

    @abstractmethod
    def generate(
        self,
        user_message: str,
        system_prompt: str | None = None,
        model: str | None = None,
        **kwargs,
    ) -> str:
        """Gửi prompt đến mô hình và nhận phản hồi."""
        pass

    def log_trace(
        self,
        provider_name: str,
        model_name: str,
        user_message: str,
        system_prompt: str | None,
        raw_response: str,
        latency_ms: float,
        error: str | None = None,
    ) -> None:
        """Ghi vết kỹ thuật vào log file phục vụ nghiệm thu CP3."""
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "provider": provider_name,
            "model": model_name,
            "latency_ms": latency_ms,
            "user_message": user_message,
            "system_prompt_excerpt": (system_prompt[:250] + "...") if system_prompt else None,
            "raw_response": raw_response,
            "error": error,
            "status": "SUCCESS" if not error else "ERROR",
        }
        try:
            with open(TRACE_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

