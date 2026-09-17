from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
DATA_DIR = ROOT / "data"
RUNS_DIR = ROOT / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)

from env_loader import load_lab_env
from providers import make_provider
from versioning import artifact_version_dict, build_artifact_version

load_lab_env(ROOT)


def normalize_text(s: str) -> str:
    if not s:
        return ""
    s = s.lower()
    s = re.sub(r"(\d{1,2})h(\d{2})", r"\1:\2", s)
    s = re.sub(r"(\d{1,2})h\b", r"\1:00", s)
    return s


def evaluate_response(response_text: str, criteria_list: list[str]) -> tuple[bool, list[str], list[str], float]:
    norm_text = normalize_text(response_text or "")
    matched = []
    missing = []
    for c in criteria_list:
        norm_c = normalize_text(c)
        # Hỗ trợ lựa chọn thay thế qua dấu |
        alts = [part.strip() for part in norm_c.split("|")]
        found = False
        for alt in alts:
            if alt in norm_text:
                found = True
                break
            words = alt.split()
            if len(words) > 1 and all(w in norm_text for w in words):
                found = True
                break
        if found:
            matched.append(c)
        else:
            missing.append(c)
    ratio = len(matched) / len(criteria_list) if criteria_list else 1.0
    return ratio >= 0.7, matched, missing, ratio


def execute_dataset(provider, model_name: str, system_prompt: str, dataset_name: str, version_tag: str, version_info):
    data_file = DATA_DIR / dataset_name
    if not data_file.is_file():
        print(f"Lỗi: Không tìm thấy tệp {data_file}")
        return None

    test_cases = json.loads(data_file.read_text(encoding="utf-8"))

    print("================================================================")
    print(f" 🚀 CHẠY KIỂM THỬ: {dataset_name} ({len(test_cases)} ca)")
    print(f" Provider: {provider.__class__.__name__} | Model: {model_name}")
    print(f" Version:  {version_info.artifact_version}")
    print("================================================================")

    results = []
    passed_count = 0
    t_start = time.time()

    for idx, tc in enumerate(test_cases, 1):
        tc_id = tc["id"]
        inp = tc["input"]
        crit = tc.get("acceptance_criteria", [])
        tax = tc.get("taxonomy_class", "unknown")

        print(f"[{idx:02d}/{len(test_cases):02d}] {tc_id} ({tax[:16]}): \"{inp[:35]}...\"", end=" -> ")
        sys.stdout.flush()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": inp},
        ]
        t0 = time.time()
        try:
            resp = provider.complete(messages, tools=None, model=model_name, temperature=0.0)
            latency = round(time.time() - t0, 2)
            reply_text = resp.text or ""
            is_pass, matched, missing, ratio = evaluate_response(reply_text, crit)
            err = None
        except Exception as e:
            latency = round(time.time() - t0, 2)
            reply_text = ""
            is_pass = False
            matched = []
            missing = crit
            err = str(e)

        if is_pass:
            passed_count += 1
            print(f"PASS ({latency}s)")
        else:
            print(f"FAIL ({latency}s)")

        results.append({
            "id": tc_id,
            "taxonomy_class": tax,
            "input": inp,
            "expected_behavior": tc.get("expected_behavior", ""),
            "criteria": crit,
            "reply": reply_text,
            "is_passed": is_pass,
            "matched": matched,
            "missing": missing,
            "latency_s": latency,
            "error": err
        })
        time.sleep(0.3)

    total_time = round(time.time() - t_start, 2)
    pass_rate = round((passed_count / len(test_cases)) * 100, 1)

    print("----------------------------------------------------------------")
    print(f" KẾT QUẢ: ĐẠT {passed_count}/{len(test_cases)} ({pass_rate}%) | Thời gian: {total_time}s")
    print("----------------------------------------------------------------\n")

    # Lưu log JSON vào runs/
    timestamp_slug = datetime.now().strftime("%Y%m%dT%H%M%S")
    dataset_slug = Path(dataset_name).stem
    provider_slug = provider.__class__.__name__.lower().replace("provider", "")
    run_filename = f"{version_tag}_B_{dataset_slug}_{provider_slug}_{timestamp_slug}.json"
    run_path = RUNS_DIR / run_filename

    run_data = {
        "timestamp": datetime.now().isoformat(),
        "provider": provider_slug,
        "model": model_name,
        "dataset": dataset_name,
        "version": artifact_version_dict(version_info),
        "total": len(test_cases),
        "passed": passed_count,
        "failed": len(test_cases) - passed_count,
        "pass_rate": pass_rate,
        "total_time_s": total_time,
        "results": results,
    }
    run_path.write_text(json.dumps(run_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Đã lưu chi tiết lượt chạy vào: runs/{run_filename}")

    # Ghi nhận vào version_log.csv
    csv_file = ARTIFACTS_DIR / "version_log.csv"
    p_hash = getattr(version_info, "prompt_hash", "")[:8]
    t_hash = getattr(version_info, "tools_hash", "")[:8]
    note = f"Chạy {dataset_slug} ({passed_count}/{len(test_cases)} PASS)"
    try:
        with open(csv_file, "a", encoding="utf-8") as f:
            f.write(f"{version_tag},{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')},p{p_hash},t{t_hash},{pass_rate}%,{note}\n")
        print(f"✅ Đã ghi nhận vào: artifacts/version_log.csv")
    except Exception:
        pass

    return run_data


def generate_combined_report(model_name: str, provider_name: str, base_run: dict | None, adv_run: dict | None):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Báo cáo Kết quả Thực thi Kiểm thử Thực tế (Run Results) — CP3 & CP4",
        "**Dự án:** Trợ lý Quy chế & Lịch nộp bài Khóa 4 (Track B)  ",
        f"**Thời điểm thực thi:** `{now_str}`  ",
        f"**Mô hình sử dụng:** `{provider_name.upper()}` · `{model_name}`  \n",
        "---\n",
        "## 1. Thống kê Định lượng Tổng hợp Cả 2 Bộ Kiểm thử\n",
        "| Bộ kiểm thử | Tổng số ca | Số ca ĐẠT (PASS) | Số ca THẤT BẠI (FAIL) | Tỷ lệ Đạt (%) | Mục đích kiểm thử |",
        "|---|---|---|---|---|---|",
    ]

    total_all = 0
    passed_all = 0

    if base_run:
        lines.append(f"| **Bộ 1: Golden Set (Chuẩn)** | **{base_run['total']} ca** | **{base_run['passed']}** | {base_run['failed']} | **{base_run['pass_rate']}%** | Tiêu chuẩn cơ bản, 50% trích xuất từ tin nhắn thật |")
        total_all += base_run['total']
        passed_all += base_run['passed']

    if adv_run:
        lines.append(f"| **Bộ 2: Nâng cao & Bẫy (Adversarial)** | **{adv_run['total']} ca** | **{adv_run['passed']}** | {adv_run['failed']} | **{adv_run['pass_rate']}%** | Chống Prompt Injection, giả mạo, teencode & đa điều kiện |")
        total_all += adv_run['total']
        passed_all += adv_run['passed']

    overall_rate = round((passed_all / total_all) * 100, 1) if total_all else 0.0
    lines.append(f"| **TỔNG CỘNG TOÀN DIỆN** | **{total_all} ca** | **{passed_all}** | {total_all - passed_all} | **{overall_rate}%** | **Đánh giá mức độ ổn định & sẵn sàng sản phẩm** |")
    lines.append("\n---\n")

    # Bảng chi tiết Bộ 1
    if base_run:
        lines.append("## 2. Bảng Kết quả Chi tiết Bộ 1: Golden Set (20 Ca Cơ bản)\n")
        lines.append("| ID | Phân loại Taxonomy | Câu hỏi kiểm thử | Kết quả | Ghi chú tiêu chí |")
        lines.append("|---|---|---|---|---|")
        for r in base_run["results"]:
            badge = "✅ PASS" if r["is_passed"] else "❌ FAIL"
            note = "Đạt tiêu chuẩn" if r["is_passed"] else f"Thiếu: {', '.join(r.get('missing', []))}"
            if r.get("error"):
                note = f"Lỗi: {r['error'][:35]}"
            lines.append(f"| **{r['id']}** | `{r.get('taxonomy_class')}` | {r['input'][:45]}... | {badge} | {note} |")
        lines.append("\n---\n")

    # Bảng chi tiết Bộ 2
    if adv_run:
        lines.append("## 3. Bảng Kết quả Chi tiết Bộ 2: Thách thức & Bẫy Nâng cao (10 Ca Adversarial)\n")
        lines.append("| ID | Phân loại Thách thức | Câu hỏi tấn công / tình huống hóc búa | Kết quả | Ghi chú phản hồi |")
        lines.append("|---|---|---|---|---|")
        for r in adv_run["results"]:
            badge = "✅ PASS" if r["is_passed"] else "❌ FAIL"
            note = "Phòng thủ thành công" if r["is_passed"] else f"Bị lừa / Thiếu: {', '.join(r.get('missing', []))}"
            if r.get("error"):
                note = f"Lỗi: {r['error'][:35]}"
            lines.append(f"| **{r['id']}** | `{r.get('taxonomy_class')}` | {r['input'][:45]}... | {badge} | {note} |")
        lines.append("\n---\n")

    # Phân tích nguyên nhân lỗi (nếu có)
    lines.append("## 4. Phân tích Các Trường hợp Cần Lưu ý & Độ Ổn Định\n")
    all_failed = []
    if base_run:
        all_failed.extend([r for r in base_run["results"] if not r["is_passed"]])
    if adv_run:
        all_failed.extend([r for r in adv_run["results"] if not r["is_passed"]])

    if not all_failed:
        lines.append("🎉 **Hoàn hảo:** Tất cả các ca kiểm thử trong cả 2 bộ đều ĐẠT chuẩn (100% PASS). Hệ thống đạt độ ổn định và an toàn cao nhất.\n")
    else:
        for f in all_failed:
            lines.append(f"### Ca {f['id']} — [{f.get('taxonomy_class')}]")
            lines.append(f"* **Câu hỏi:** \"{f['input']}\"")
            lines.append(f"* **Tiêu chí thiếu:** `{f.get('missing')}`")
            lines.append(f"* **Phản hồi thực tế từ mô hình:**")
            lines.append(f"> {f.get('reply', '')[:250]}...")
            lines.append("")

    report_text = "\n".join(lines)

    # Ghi file eval/run_results.md
    eval_file = ROOT.parent / "eval" / "run_results.md"
    try:
        eval_file.write_text(report_text, encoding="utf-8")
        print(f"✅ Đã xuất báo cáo tổng hợp vào: {eval_file}")
    except Exception as e:
        print(f"Lỗi ghi {eval_file}: {e}")

    # Ghi file codebase/artifacts/REPORT.md
    art_file = ARTIFACTS_DIR / "REPORT.md"
    try:
        art_file.write_text(report_text, encoding="utf-8")
        print(f"✅ Đã xuất báo cáo tổng hợp vào: {art_file}")
    except Exception as e:
        print(f"Lỗi ghi {art_file}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Chạy kiểm thử đánh giá mô hình.")
    parser.add_argument("--provider", default="openrouter", choices=["openrouter", "openai", "gemini", "groq"])
    parser.add_argument("--model", default=None, help="Mô hình LLM")
    parser.add_argument("--data", default="eval_base.json", help="Tệp dữ liệu trong data/ (mặc định eval_base.json)")
    parser.add_argument("--version", default="v2", help="Phiên bản prompt (v0, v1, v2)")
    parser.add_argument("--all", action="store_true", help="Chạy cả 2 bộ: Bộ cơ bản (20 ca) và Bộ nâng cao (10 ca)")
    args = parser.parse_args()

    provider = make_provider(args.provider)
    model_name = args.model or getattr(provider, "default_model", "openai/gpt-4o-mini")

    prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"
    system_prompt = prompt_path.read_text(encoding="utf-8") if prompt_path.is_file() else ""
    version_info = build_artifact_version(args.version, prompt_path, tools_path)

    if args.all:
        print("\n🚀 BẮT ĐẦU CHẠY KIỂM THỬ TOÀN DIỆN CẢ 2 BỘ (30 CA TỔNG CỘNG)...")
        base_run = execute_dataset(provider, model_name, system_prompt, "eval_base.json", args.version, version_info)
        adv_run = execute_dataset(provider, model_name, system_prompt, "eval_adversarial.json", f"{args.version}_adv", version_info)
        generate_combined_report(model_name, args.provider, base_run, adv_run)
    else:
        run = execute_dataset(provider, model_name, system_prompt, args.data, args.version, version_info)
        if "adv" in args.data:
            generate_combined_report(model_name, args.provider, None, run)
        else:
            generate_combined_report(model_name, args.provider, run, None)


if __name__ == "__main__":
    main()
