from pathlib import Path

import pytest
from PIL import Image

from scripts.normalize_raster import normalize


def test_cover_transposes_alpha_and_reports_hashes(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    output = tmp_path / "final.png"
    image = Image.new("RGBA", (1600, 900), (255, 0, 0, 180))
    image.save(source)

    report = normalize(source, output, 1080, 1920, fit_mode="cover")

    assert report["final_size"] == [1080, 1920]
    assert report["mode"] == "RGB"
    assert report["text_layer_added"] is False
    assert report["ocr_check"] == "not_run"
    assert len(report["input_sha256"]) == 64
    assert len(report["output_sha256"]) == 64
    with Image.open(output) as result:
        assert result.size == (1080, 1920)
        assert result.mode == "RGB"


def test_pad_and_overwrite_are_explicit(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    output = tmp_path / "final.png"
    Image.new("RGB", (100, 200), "white").save(source)

    normalize(source, output, 108, 192, fit_mode="pad")
    with pytest.raises(FileExistsError):
        normalize(source, output, 108, 192, fit_mode="pad")
    normalize(source, output, 108, 192, fit_mode="pad", overwrite=True)


def test_same_input_and_output_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    Image.new("RGB", (10, 10), "black").save(source)

    with pytest.raises(ValueError, match="different"):
        normalize(source, source, 10, 10)
