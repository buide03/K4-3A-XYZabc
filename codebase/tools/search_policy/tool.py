from __future__ import annotations
from pathlib import Path
from typing import Any
from tools._shared import ROOT, terms

POLICY_DIR = ROOT / "course_policy"

def search_policy(query: str) -> dict[str, Any]:
    """Tra cứu các tệp markdown quy chế trong course_policy."""
    query_terms = terms(query)
    matches = []
    
    if POLICY_DIR.is_dir():
        for file in POLICY_DIR.glob("*.md"):
            if file.name == "README.md":
                continue
            content = file.read_text(encoding="utf-8")
            file_terms = terms(content)
            overlap = query_terms.intersection(file_terms)
            if overlap or not query_terms:
                matches.append({
                    "file": file.name,
                    "relevance_score": len(overlap),
                    "snippet": content[:300].strip() + "..."
                })

    matches.sort(key=lambda x: x["relevance_score"], reverse=True)
    return {
        "status": "success",
        "query": query,
        "results": matches[:2]
    }

