from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
from typing import Any

from providers.base import ModelResponse, ToolCall


class OpenAIProvider:
    """OpenAI Chat Completions provider with normalized tool_calls output."""

    def __init__(
        self,
        *,
        api_key_env: str = "OPENAI_API_KEY",
        base_url: str | None = None,
        default_model: str = "gpt-4o-mini",
    ) -> None:
        self.api_key_env = api_key_env
        if not os.getenv(self.api_key_env):
            try:
                from env_loader import load_lab_env
                from pathlib import Path
                load_lab_env(Path(__file__).resolve().parent.parent)
            except Exception:
                pass
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.default_model = default_model

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tool_choice: Any | None = None,
    ) -> ModelResponse:
        # Ưu tiên dùng SDK openai nếu có
        try:
            from openai import OpenAI
            api_key = os.getenv(self.api_key_env)
            if not api_key:
                raise RuntimeError(f"Missing API key env var: {self.api_key_env}")

            client = OpenAI(api_key=api_key, base_url=self.base_url)
            kwargs: dict[str, Any] = {
                "model": model or self.default_model,
                "messages": messages,
                "temperature": temperature,
            }
            if tools:
                kwargs["tools"] = tools
            if tool_choice is not None:
                kwargs["tool_choice"] = tool_choice

            resp = client.chat.completions.create(**kwargs)
            msg = resp.choices[0].message
            calls: list[ToolCall] = []
            for call in msg.tool_calls or []:
                args = json.loads(call.function.arguments or "{}")
                calls.append(ToolCall(name=call.function.name, args=args))
            return ModelResponse(text=msg.content, tool_calls=calls, raw=resp)
        except ImportError:
            # Fallback sang HTTP request chuẩn không cần cài thư viện openai
            api_key = os.getenv(self.api_key_env)
            if not api_key:
                raise RuntimeError(f"Missing API key env var: {self.api_key_env}")

            endpoint = f"{self.base_url.rstrip('/')}/chat/completions"
            payload: dict[str, Any] = {
                "model": model or self.default_model,
                "messages": messages,
                "temperature": temperature,
            }
            if tools:
                payload["tools"] = tools
            if tool_choice is not None:
                payload["tool_choice"] = tool_choice

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/buide03/K4-3A-XYZabc",
                "X-Title": "Course-Assistant-B04",
            }
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choice = data["choices"][0]["message"]
                calls: list[ToolCall] = []
                for call in choice.get("tool_calls") or []:
                    fn = call.get("function", {})
                    args = json.loads(fn.get("arguments") or "{}")
                    calls.append(ToolCall(name=fn.get("name", ""), args=args))
                return ModelResponse(text=choice.get("content"), tool_calls=calls, raw=data)

    def generate(
        self,
        user_message: str,
        system_prompt: str | None = None,
        model: str | None = None,
        **kwargs,
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})
        resp = self.complete(messages, model=model, **kwargs)
        return resp.text or ""
