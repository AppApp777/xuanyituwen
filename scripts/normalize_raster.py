#!/usr/bin/env python3
"""Normalize a no-text raster without adding overlays or claiming OCR inspection."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Optional, Tuple

from PIL import Image, ImageOps


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _crop_box(size: Tuple[int, int], target: Tuple[int, int], focus: Tuple[float, float]) -> Optional[Tuple[int, int, int, int]]:
    source_width, source_height = size
    target_width, target_height = target
    source_ratio = source_width / source_height
    target_ratio = target_width / target_height
    if abs(source_ratio - target_ratio) < 1e-9:
        return None

    if source_ratio > target_ratio:
        crop_height = source_height
        crop_width = max(1, round(source_height * target_ratio))
    else:
        crop_width = source_width
        crop_height = max(1, round(source_width / target_ratio))

    left = round((source_width - crop_width) * focus[0])
    top = round((source_height - crop_height) * focus[1])
    left = min(max(0, left), source_width - crop_width)
    top = min(max(0, top), source_height - crop_height)
    return (left, top, left + crop_width, top + crop_height)


def _flatten(image: Image.Image, background: Tuple[int, int, int]) -> Image.Image:
    rgba = image.convert("RGBA")
    canvas = Image.new("RGBA", rgba.size, (*background, 255))
    return Image.alpha_composite(canvas, rgba).convert("RGB")


def _render(
    source: Image.Image,
    width: int,
    height: int,
    fit_mode: str,
    focus: Tuple[float, float],
    background: Tuple[int, int, int],
) -> Tuple[Image.Image, Optional[Tuple[int, int, int, int]], float]:
    target = (width, height)
    oriented = ImageOps.exif_transpose(source).convert("RGBA")
    source_size = oriented.size
    crop_box = _crop_box(source_size, target, focus) if fit_mode == "cover" else None

    if fit_mode == "cover":
        rendered = ImageOps.fit(
            oriented,
            target,
            method=Image.Resampling.LANCZOS,
            centering=focus,
        )
        scale = max(width / source_size[0], height / source_size[1])
    else:
        contained = ImageOps.contain(oriented, target, method=Image.Resampling.LANCZOS)
        scale = min(width / source_size[0], height / source_size[1])
        if fit_mode == "contain":
            rendered = contained
        else:
            rendered = Image.new("RGBA", target, (*background, 255))
            left = (width - contained.width) // 2
            top = (height - contained.height) // 2
            rendered.alpha_composite(contained, (left, top))

    return _flatten(rendered, background), crop_box, scale


def normalize(
    input_path: Path,
    output_path: Path,
    width: int,
    height: int,
    fit_mode: str = "cover",
    focus: Tuple[float, float] = (0.5, 0.5),
    background: Tuple[int, int, int] = (0, 0, 0),
    overwrite: bool = False,
) -> dict[str, Any]:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    if fit_mode not in {"cover", "contain", "pad"}:
        raise ValueError("fit_mode must be cover, contain, or pad")
    if not all(0 <= value <= 1 for value in focus):
        raise ValueError("focus values must be between 0 and 1")
    if input_path.resolve() == output_path.resolve():
        raise ValueError("input and output paths must be different")
    if not input_path.is_file():
        raise FileNotFoundError(input_path)
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output_path}; pass --overwrite to replace it")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(input_path) as source:
        original_size = list(ImageOps.exif_transpose(source).size)
        final, crop_box, scale = _render(source, width, height, fit_mode, focus, background)
        final.save(output_path, format="PNG", optimize=True)

    return {
        "input": str(input_path),
        "output": str(output_path),
        "original_size": original_size,
        "final_size": [width, height],
        "mode": "RGB",
        "fit_mode": fit_mode,
        "focus": list(focus),
        "crop_box": list(crop_box) if crop_box else None,
        "scale": scale,
        "input_sha256": _sha256(input_path),
        "output_sha256": _sha256(output_path),
        "text_layer_added": False,
        "ocr_check": "not_run",
    }


def _hex_color(value: str) -> Tuple[int, int, int]:
    normalized = value.removeprefix("#")
    if len(normalized) != 6:
        raise ValueError("background must be a six-digit hex color")
    try:
        return tuple(int(normalized[index : index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]
    except ValueError as exc:
        raise ValueError("background must be a six-digit hex color") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="将纯净无字底图归一化为 RGB PNG，不添加文字或图层。")
    parser.add_argument("--input", required=True, type=Path, help="输入无字图片路径。")
    parser.add_argument("--output", required=True, type=Path, help="输出 PNG 路径。")
    parser.add_argument("--width", type=int, default=1080, help="输出宽度，默认 1080。")
    parser.add_argument("--height", type=int, default=1920, help="输出高度，默认 1920。")
    parser.add_argument("--fit", choices=("cover", "contain", "pad"), default="cover", help="裁切或留白策略，默认 cover。")
    parser.add_argument("--focus-x", type=float, default=0.5, help="cover 裁切焦点横坐标，范围 0 到 1。")
    parser.add_argument("--focus-y", type=float, default=0.5, help="cover 裁切焦点纵坐标，范围 0 到 1。")
    parser.add_argument("--background", default="000000", help="contain 或 pad 使用的六位十六进制背景色。")
    parser.add_argument("--overwrite", action="store_true", help="允许覆盖已存在的输出文件。")
    args = parser.parse_args()

    try:
        result = normalize(
            args.input,
            args.output,
            args.width,
            args.height,
            fit_mode=args.fit,
            focus=(args.focus_x, args.focus_y),
            background=_hex_color(args.background),
            overwrite=args.overwrite,
        )
    except (OSError, ValueError) as exc:
        print(f"图像归一化失败：{exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
