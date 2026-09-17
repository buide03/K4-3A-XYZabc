from __future__ import annotations
import time
from typing import Any

def create_ticket(issue_type: str, summary: str) -> dict[str, Any]:
    """Tạo ticket chuyển tiếp cho Trợ giảng (TA) qua hệ thống TA-Bridge."""
    ticket_id = f"TICK-{int(time.time()) % 100000:05d}"
    return {
        "status": "ticket_created",
        "ticket_id": ticket_id,
        "issue_type": issue_type,
        "summary": summary,
        "message": f"Đã tạo ticket {ticket_id} gửi tới Trợ giảng (@E403_TA). TA sẽ phản hồi học viên tại kênh hỗ trợ trong thời gian sớm nhất."
    }

