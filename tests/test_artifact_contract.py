import json
from pathlib import Path

from PIL import Image

from scripts.validate_artifact_package import validate_package


def _write_valid_package(root: Path) -> None:
    for directory in ("prompts", "base", "final"):
        (root / directory).mkdir(parents=True)
    for name in ("story-control.md", "frame-plan.md", "spatial-anchor-ledger.md"):
        (root / name).write_text("# fixture\nEVID-01\n", encoding="utf-8")
    (root / "captions.md").write_text(
        "## FRAME-01\n- 关联图片：`final/frame-01.png`\n- 画面事实引用：`EVID-01`\n",
        encoding="utf-8",
    )
    (root / "prompts" / "frame-01.txt").write_text("PROMPT-01\n", encoding="utf-8")
    for directory in ("base", "final"):
        Image.new("RGB", (1080, 1920), "black").save(root / directory / "frame-01.png")
    (root / "manifest.json").write_text(
        json.dumps(
            {
                "frames": [{"id": "FRAME-01", "image": "final/frame-01.png", "prompt": "prompts/frame-01.txt", "caption": "captions.md#frame-01"}],
                "definitions": {"evidence": ["EVID-01"]},
                "image_spec": {"text_layer_added": False, "ocr_check": "not_run"},
                "quality": {
                    "ending": {
                        "frame": "FRAME-01",
                        "result": "pass",
                        "evidence": "final/frame-01.png",
                        "subject_bbox": [0.1, 0.05, 0.8, 0.8],
                        "focal_count": 1,
                        "thumbnail": {"width": 270, "height": 480, "recognizable": True},
                    }
                },
            }
        ),
        encoding="utf-8",
    )


def test_valid_package_passes_strict_checks(tmp_path: Path) -> None:
    _write_valid_package(tmp_path)

    report = validate_package(tmp_path, strict=True)

    assert report["passed"] is True
    assert report["errors"] == []


def test_undefined_evidence_is_reported(tmp_path: Path) -> None:
    _write_valid_package(tmp_path)
    (tmp_path / "captions.md").write_text(
        "## FRAME-01\n- 关联图片：`final/frame-01.png`\n- 画面事实引用：`EVID-99`\n",
        encoding="utf-8",
    )

    report = validate_package(tmp_path, strict=False)

    assert report["passed"] is False
    assert any("未定义的证据" in error for error in report["errors"])


def test_ending_gate_rejects_small_subject_without_exception(tmp_path: Path) -> None:
    _write_valid_package(tmp_path)
    manifest_path = tmp_path / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["quality"]["ending"]["subject_bbox"] = [0.1, 0.1, 0.4, 0.4]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    report = validate_package(tmp_path, strict=True)

    assert report["passed"] is False
    assert any("主体面积低于最低阈值" in error for error in report["errors"])
