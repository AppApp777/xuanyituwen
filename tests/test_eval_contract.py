from pathlib import Path

from scripts.validate_evals import validate_evals


def test_evals_and_fixtures_are_complete() -> None:
    report = validate_evals(Path("evals/evals.json"))

    assert report["passed"] is True, report["errors"]
    assert report["cases"] == 5
