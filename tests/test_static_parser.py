from pathlib import Path

from r2t2.static_parser import locate_references


HERE = Path(__file__).parent
SAMPLE_PATH = HERE / "fixtures/sample_code.py"


class TestLocateReferences:
    def test_accepts_str(self, bib_with_tracking):
        locate_references(str(SAMPLE_PATH))
        assert "Great British Roasts, 2019" in bib_with_tracking.references

    def test_accepts_path(self, bib_with_tracking):
        locate_references(SAMPLE_PATH)
        assert "Great British Roasts, 2019" in bib_with_tracking.references
