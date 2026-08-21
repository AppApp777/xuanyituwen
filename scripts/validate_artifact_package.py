#!/usr/bin/env python3
"""Validate the cheap, machine-checkable part of a xuanyituwen output package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

try:
    from PIL import Image
except ImportError:  # pragma: no cover - the CLI reports a useful error below.
    Image = None  # type: ignore[assignment,misc]


FRAME_FILE_RE = re.compile(r"^frame-(\d{2})\.(png|jpg|jpeg|webp)$", re.IGNORECASE)
PROMPT_FILE_RE = re.compile(r"^frame-(\d{2})\.txt$", re.IGNORECASE)
FRAME_TOKEN_RE = re.compile(r"\bFRAME-(\d{2})\b")
EVID_TOKEN_RE = re.compile(r"\bEVID-(\d{2,})\b")


def _frame_numbers(directory: Path, pattern: re.Pattern[str]) -> Set[int]:
    if not directory.is_dir():
        return set()
    numbers: Set[int] = set()
    for path in directory.iterdir():
        match = pattern.match(path.name)
        if match:
            numbers.add(int(match.group(1)))
    return numbers


def _frame_tokens(text: str) -> Set[int]:
    return {int(match.group(1)) for match in FRAME_TOKEN_RE.finditer(text)}


def _read_manifest(path: Path, errors: List[str]) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"manifest.json 无法读取：{exc}")
        return {}
    if not isinstance(value, dict):
        errors.append("manifest.json 顶层必须是对象")
        return {}
    return value


def _validate_manifest(manifest: Dict[str, Any], frames: Set[int], strict: bool, errors: List[str]) -> None:
    if not manifest:
        if strict:
            errors.append("strict 模式要求 manifest.json")
        return
    entries = manifest.get("frames")
    if entries is None:
        if strict:
            errors.append("strict 模式要求 manifest.frames")
        return
    if not isinstance(entries, list):
        errors.append("manifest.frames 必须是数组")
        return

    seen: Set[int] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("manifest.frames 中存在非对象项")
            continue
        frame_id = entry.get("id", "")
        match = re.fullmatch(r"FRAME-(\d{2})", str(frame_id))
        if not match:
            errors.append(f"manifest 中存在非法 FRAME ID：{frame_id}")
            continue
        number = int(match.group(1))
        if number in seen:
            errors.append(f"manifest 重复登记 FRAME-{number:02d}")
        seen.add(number)
        expected = {
            "image": f"final/frame-{number:02d}.png",
            "prompt": f"prompts/frame-{number:02d}.txt",
            "caption": f"captions.md#frame-{number:02d}",
        }
        for key, value in expected.items():
            allowed = (value, f"base/frame-{number:02d}.png") if key == "image" else (value,)
            if entry.get(key) not in allowed:
                errors.append(f"FRAME-{number:02d} 的 manifest.{key} 未绑定到预期文件")

    if frames and seen != frames:
        errors.append(f"manifest FRAME 集合 {sorted(seen)} 与图片集合 {sorted(frames)} 不一致")


def _validate_image_spec(manifest: Dict[str, Any], strict: bool, errors: List[str]) -> None:
    image_spec = manifest.get("image_spec")
    if image_spec is None:
        if strict:
            errors.append("strict 模式要求 manifest.image_spec")
        return
    if not isinstance(image_spec, dict):
        errors.append("manifest.image_spec 必须是对象")
        return
    if image_spec.get("text_layer_added") is not False:
        errors.append("manifest.image_spec.text_layer_added 必须明确为 false")
    if image_spec.get("ocr_check") != "not_run":
        errors.append("manifest.image_spec.ocr_check 必须明确为 not_run，不能把未运行 OCR 写成通过")


def _validate_ending_gate(manifest: Dict[str, Any], frames: Set[int], strict: bool, errors: List[str]) -> None:
    quality = manifest.get("quality")
    ending = quality.get("ending") if isinstance(quality, dict) else None
    if not isinstance(ending, dict):
        if strict:
            errors.append("strict 模式要求 manifest.quality.ending")
        return

    expected_frame = f"FRAME-{max(frames):02d}" if frames else ""
    if ending.get("frame") != expected_frame:
        errors.append(f"终局验收必须绑定最后一张 {expected_frame}")
    if ending.get("result") != "pass":
        errors.append("manifest.quality.ending.result 必须是 pass")
    if not ending.get("evidence"):
        errors.append("终局验收必须填写 evidence")

    bbox = ending.get("subject_bbox")
    if not isinstance(bbox, list) or len(bbox) != 4 or not all(isinstance(value, (int, float)) for value in bbox):
        errors.append("终局验收的 subject_bbox 必须是归一化 [x, y, width, height]")
    else:
        x, y, width, height = [float(value) for value in bbox]
        if min(x, y, width, height) < 0 or x + width > 1 or y + height > 1 or width <= 0 or height <= 0:
            errors.append("终局验收的 subject_bbox 必须位于 0 到 1 的画布范围内")
        minimum_area = ending.get("minimum_subject_area", 0.60)
        if not isinstance(minimum_area, (int, float)) or not 0 < minimum_area <= 1:
            errors.append("终局验收的 minimum_subject_area 必须在 0 到 1 之间")
        elif width * height < float(minimum_area) and not ending.get("exception_reason"):
            errors.append("终局主体面积低于最低阈值，需补充 exception_reason 或重新构图")

    if ending.get("focal_count") != 1:
        errors.append("终局验收的 focal_count 必须是 1")
    thumbnail = ending.get("thumbnail")
    if not isinstance(thumbnail, dict) or thumbnail.get("width") != 270 or thumbnail.get("height") != 480:
        errors.append("终局验收必须记录固定 270×480 缩略图规格")
    elif thumbnail.get("recognizable") is not True:
        errors.append("终局验收必须明确记录缩略图主体可识别")


def _validate_images(directory: Path, frames: Iterable[int], strict: bool, errors: List[str], warnings: List[str]) -> None:
    if not directory.is_dir():
        if strict:
            errors.append(f"缺少图片目录：{directory.name}/")
        return
    if Image is None:
        errors.append("校验图片需要 Pillow，请先安装 requirements.txt")
        return

    for number in sorted(frames):
        path = directory / f"frame-{number:02d}.png"
        if not path.is_file():
            if strict:
                errors.append(f"缺少图片：{path.relative_to(directory.parent)}")
            continue
        try:
            with Image.open(path) as image:
                if strict and (image.size != (1080, 1920) or image.mode != "RGB"):
                    errors.append(f"{path.name} 必须是 1080×1920 RGB，实际为 {image.size} {image.mode}")
        except OSError as exc:
            errors.append(f"图片无法读取：{path}，{exc}")

    if not strict:
        warnings.append(f"未执行 1080×1920 RGB 图片规格检查：{directory.name}/")


def validate_package(root: Path, strict: bool = False) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []
    required_files = ("story-control.md", "frame-plan.md", "captions.md", "spatial-anchor-ledger.md")
    for name in required_files:
        if not (root / name).is_file():
            errors.append(f"缺少交付文件：{name}")

    if strict:
        for directory in ("prompts", "base", "final"):
            if not (root / directory).is_dir():
                errors.append(f"缺少交付目录：{directory}/")

    final_frames = _frame_numbers(root / "final", FRAME_FILE_RE)
    base_frames = _frame_numbers(root / "base", FRAME_FILE_RE)
    prompt_frames = _frame_numbers(root / "prompts", PROMPT_FILE_RE)
    captions_text = (root / "captions.md").read_text(encoding="utf-8") if (root / "captions.md").is_file() else ""
    caption_frames = _frame_tokens(captions_text)
    available = final_frames or base_frames or prompt_frames or caption_frames
    if not available:
        errors.append("没有找到任何 FRAME 交付记录")
        available = set()

    if available:
        expected = set(range(1, max(available) + 1))
        if available != expected:
            errors.append(f"FRAME 编号必须从 FRAME-01 连续到最大编号，实际为 {sorted(available)}")
    for label, values in (("base", base_frames), ("final", final_frames), ("prompts", prompt_frames), ("captions", caption_frames)):
        if (strict or values) and values != available:
            errors.append(f"{label} 的 FRAME 集合 {sorted(values)} 与主集合 {sorted(available)} 不一致")

    for number in sorted(available):
        marker = f"FRAME-{number:02d}"
        expected_image = f"final/frame-{number:02d}.png"
        if captions_text and marker in captions_text and expected_image not in captions_text:
            errors.append(f"captions.md 中的 {marker} 缺少关联图片路径 {expected_image}")

    manifest = _read_manifest(root / "manifest.json", errors)
    _validate_manifest(manifest, available, strict, errors)
    _validate_image_spec(manifest, strict, errors)
    _validate_ending_gate(manifest, available, strict, errors)
    definitions = manifest.get("definitions", {}) if isinstance(manifest, dict) else {}
    evidence_ids = set(definitions.get("evidence", [])) if isinstance(definitions, dict) else set()
    if evidence_ids:
        referenced = {f"EVID-{number}" for number in EVID_TOKEN_RE.findall(captions_text)}
        missing = sorted(referenced - evidence_ids)
        if missing:
            errors.append(f"captions.md 引用了未定义的证据 ID：{', '.join(missing)}")

    _validate_images(root / "final", available, strict, errors, warnings)
    report = {
        "package": str(root),
        "frames": [f"FRAME-{number:02d}" for number in sorted(available)],
        "errors": errors,
        "warnings": warnings,
        "passed": not errors,
        "strict": strict,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="检查 xuanyituwen 产物包的编号、文件绑定和图片规格。")
    parser.add_argument("package", type=Path, help="故事输出包目录。")
    parser.add_argument("--strict", action="store_true", help="要求 prompts、base、final 和 1080×1920 RGB PNG。")
    parser.add_argument("--json", action="store_true", help="只输出 JSON 报告。")
    args = parser.parse_args()
    report = validate_package(args.package, strict=args.strict)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if report["warnings"]:
            print("提示：" + "；".join(report["warnings"]), file=sys.stderr)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
