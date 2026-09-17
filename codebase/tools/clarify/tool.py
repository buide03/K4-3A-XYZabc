from __future__ import annotations
from typing import Any

def ask_user(topic: str, suggested_options: list[str]) -> dict[str, Any]:
    """Hỏi lại học viên để làm rõ câu hỏi mơ hồ giữa các hệ thống."""
    return {
        "status": "clarification_requested",
        "topic": topic,
        "options": suggested_options,
        "message": f"Hệ thống nhận thấy câu hỏi về '{topic}' có thể áp dụng cho nhiều quy chế khác nhau. Bạn vui lòng chọn ngữ cảnh cụ thể: {', '.join(suggested_options)}."
    }

