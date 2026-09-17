"""
LLM Client: Multi-provider Unified Adapter
Hỗ trợ chuyển đổi mượt mà giữa: OpenRouter, Google Gemini, OpenAI và OpenAI-compatible.
Sử dụng urllib chuẩn của Python, không phụ thuộc thư viện bên ngoài.
Tích hợp sẵn hệ thống Logging ghi vết Prompt & Raw Response phục vụ nghiệm thu CP3.
"""

import os
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

# Thư mục ghi log vết phục vụ chấm điểm kỹ thuật CP3
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
TRACE_LOG_FILE = LOG_DIR / "llm_trace.jsonl"


def load_env_file(filepath=None):
    """Đọc tệp .env nếu có mà không cần thư viện python-dotenv"""
    if filepath is None:
        # Tìm .env ở thư mục gốc repo hoặc thư mục codebase
        candidates = [
            Path(__file__).resolve().parent.parent / ".env",
            Path(__file__).resolve().parent / ".env",
        ]
        for c in candidates:
            if c.is_file():
                filepath = c
                break
    
    if filepath and Path(filepath).is_file():
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if key and key not in os.environ:
                    os.environ[key] = val


# Tự động nạp .env khi import
load_env_file()


class UnifiedLLMClient:
    def __init__(self, provider=None, model=None, api_key=None):
        # Nạp lại env nếu vừa cập nhật
        load_env_file()
        
        self.provider = (provider or os.getenv("LLM_PROVIDER", "openrouter")).lower().strip()
        self.api_key = api_key or self._get_default_api_key(self.provider)
        self.model = model or self._get_default_model(self.provider)
        self.temperature = float(os.getenv("TEMPERATURE", "0.1"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000"))

    def _get_default_api_key(self, provider):
        if provider == "openrouter":
            return os.getenv("OPENROUTER_API_KEY", "")
        elif provider == "gemini":
            return os.getenv("GEMINI_API_KEY", "")
        elif provider == "openai":
            return os.getenv("OPENAI_API_KEY", "")
        return os.getenv("LLM_API_KEY", "")

    def _get_default_model(self, provider):
        if provider == "openrouter":
            return os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        elif provider == "gemini":
            return os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        elif provider == "openai":
            return os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return os.getenv("LLM_MODEL", "default")

    def switch_provider(self, provider, api_key=None, model=None):
        """Cho phép đổi provider trong lúc chạy chỉ bằng 1 dòng lệnh"""
        self.provider = provider.lower().strip()
        self.api_key = api_key or self._get_default_api_key(self.provider)
        self.model = model or self._get_default_model(self.provider)

    def generate(self, user_message, system_prompt=None):
        """Gửi prompt đến mô hình đã chọn và ghi log vết thực tế"""
        start_time = time.time()
        raw_response = ""
        error_msg = None

        if not self.api_key or self.api_key.startswith("your_"):
            raise ValueError(
                f"Chưa cấu hình API Key hợp lệ cho provider '{self.provider}'. "
                f"Vui lòng cập nhật API key trong tệp .env (hoặc biến môi trường {self.provider.upper()}_API_KEY)."
            )

        try:
            if self.provider == "openrouter":
                raw_response = self._call_openrouter(user_message, system_prompt)
            elif self.provider == "gemini":
                raw_response = self._call_gemini(user_message, system_prompt)
            elif self.provider == "openai":
                raw_response = self._call_openai(user_message, system_prompt)
            else:
                raw_response = self._call_openrouter(user_message, system_prompt)
        except Exception as e:
            error_msg = str(e)
            raise e
        finally:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            self._log_trace(
                user_message=user_message,
                system_prompt=system_prompt,
                raw_response=raw_response,
                error=error_msg,
                latency_ms=latency_ms
            )

        return raw_response

    def _call_openrouter(self, user_message, system_prompt):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/buide03/K4-3A-XYZabc",
            "X-Title": "Course-Assistant-B04",
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]

    def _call_gemini(self, user_message, system_prompt):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        contents = []
        if system_prompt:
            contents.append({
                "role": "user",
                "parts": [{"text": f"[System Context / Instructions]:\n{system_prompt}\n\nPlease strictly follow instructions above."}]
            })
            contents.append({
                "role": "model",
                "parts": [{"text": "Tôi đã hiểu rõ toàn bộ quy chế và nguyên tắc. Xin mời học viên đặt câu hỏi."}]
            })
        
        contents.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens,
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]

    def _call_openai(self, user_message, system_prompt):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]

    def _log_trace(self, user_message, system_prompt, raw_response, error, latency_ms):
        """Ghi vết kỹ thuật vào file JSON Lines phục vụ xác minh CP3"""
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "provider": self.provider,
            "model": self.model,
            "latency_ms": latency_ms,
            "user_message": user_message,
            "system_prompt_excerpt": (system_prompt[:250] + "...") if system_prompt else None,
            "raw_response": raw_response,
            "error": error,
            "status": "SUCCESS" if not error else "ERROR"
        }
        try:
            with open(TRACE_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

