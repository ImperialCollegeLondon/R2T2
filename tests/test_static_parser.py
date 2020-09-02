from pathlib import Path

from r2t2.static_parser import locate_references


HERE = Path(__file__).parent
FIXTURES = HERE / "fixtures"
SAMPLE_PATH = FIXTURES / "sample_code.py"


class TestLocateReferences:
    def test_accepts_str(self, bib_with_tracking):
        locate_references(str(SAMPLE_PATH))
        assert "Great British Roasts, 2019" in bib_with_tracking.references

    def test_accepts_path(self, bib_with_tracking):
        locate_references(SAMPLE_PATH)
        assert "Great British Roasts, 2019" in bib_with_tracking.references

    def test_globs_for_folder(self, bib_with_tracking):
        locate_references(FIXTURES)
        assert "Great British Roasts, 2019" in bib_with_tracking.references
