#!/usr/bin/env python3
"""Normalize a no-text raster to a portrait RGB PNG without adding overlays."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps


def normalize(input_path: Path, output_path: Path, width: int, height: int) -> dict[str, object]:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")

    with Image.open(input_path) as source:
        fitted = ImageOps.fit(
            source.convert("RGBA"),
            (width, height),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )
        final = fitted.convert("RGB")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final.save(output_path, format="PNG", optimize=True)

    return {
        "input": str(input_path),
        "output": str(output_path),
        "width": width,
        "height": height,
        "mode": "RGB",
        "embedded_text": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="将纯净无字底图归一化为 RGB 竖屏 PNG，不添加任何文字或图层。"
    )
    parser.add_argument("--input", required=True, type=Path, help="输入无字图片路径。")
    parser.add_argument("--output", required=True, type=Path, help="输出 PNG 路径。")
    parser.add_argument("--width", type=int, default=1080, help="输出宽度，默认 1080。")
    parser.add_argument("--height", type=int, default=1920, help="输出高度，默认 1920。")
    args = parser.parse_args()

    try:
        result = normalize(args.input, args.output, args.width, args.height)
    except (OSError, ValueError) as exc:
        print(f"图像归一化失败：{exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
