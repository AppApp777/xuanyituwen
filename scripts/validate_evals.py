#!/usr/bin/env python3
"""Validate the lightweight, fixture-backed evaluation contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_FIELDS = (
    "id",
    "case_version",
    "name",
    "stage",
    "prompt",
    "fixture_paths",
    "allowed_actions",
    "forbidden_actions",
    "machine_assertions",
    "judge_rubric",
    "pass_threshold",
    "baseline_prompt",
    "trials",
    "model_environment",
)


def validate_evals(path: Path) -> Dict[str, Any]:
    errors: List[str] = []
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"passed": False, "errors": [f"无法读取评测文件：{exc}"], "cases": 0}

    if document.get("skill_name") != "xuanyituwen":
        errors.append("skill_name 必须是 xuanyituwen")
    policy = document.get("evaluation_policy", {})
    if policy.get("trigger_evaluation") is not False:
        errors.append("触发准确性评测必须保持关闭")
    cases = document.get("evals")
    if not isinstance(cases, list) or len(cases) < 5:
        errors.append("至少需要五个阶段评测用例")
        cases = []

    seen_ids = set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append("评测用例必须是对象")
            continue
        missing = [field for field in REQUIRED_FIELDS if field not in case]
        if missing:
            errors.append(f"{case.get('id', '<unknown>')} 缺少字段：{', '.join(missing)}")
        case_id = case.get("id")
        if case_id in seen_ids:
            errors.append(f"评测 ID 重复：{case_id}")
        seen_ids.add(case_id)
        threshold = case.get("pass_threshold")
        if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1:
            errors.append(f"{case_id} 的 pass_threshold 必须在 0 到 1 之间")
        for fixture in case.get("fixture_paths", []):
            if not (path.parent.parent / fixture).is_file():
                errors.append(f"{case_id} 缺少夹具：{fixture}")
        if not case.get("machine_assertions"):
            errors.append(f"{case_id} 至少需要一个机器断言")
        if not case.get("judge_rubric"):
            errors.append(f"{case_id} 至少需要一个模型或人工评分项")

    return {"passed": not errors, "errors": errors, "cases": len(cases)}


def main() -> int:
    parser = argparse.ArgumentParser(description="检查 xuanyituwen 的评测配置和固定夹具。")
    parser.add_argument("path", type=Path, nargs="?", default=Path("evals/evals.json"))
    args = parser.parse_args()
    report = validate_evals(args.path)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
