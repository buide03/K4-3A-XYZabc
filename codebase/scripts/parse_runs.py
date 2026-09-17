from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT / "runs"


def main() -> None:
    if not RUNS_DIR.exists():
        print("Thư mục runs/ chưa có tệp kết quả nào.")
        return

    runs = list(RUNS_DIR.glob("*.json"))
    if not runs:
        print("Chưa có lượt chạy nào trong runs/.")
        return

    print(f"Tổng số tệp kết quả: {len(runs)}")
    for r in runs:
        try:
            data = json.loads(r.read_text(encoding="utf-8"))
            passed = data.get("passed", 0)
            total = data.get("total", 0)
            rate = data.get("pass_rate", 0)
            print(f"- {r.name}: Đạt {passed}/{total} ({rate}%) | Model: {data.get('model')}")
        except Exception:
            pass


if __name__ == "__main__":
    main()

