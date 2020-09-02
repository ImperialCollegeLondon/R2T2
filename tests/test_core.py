import pytest


@pytest.fixture
def chicken():
    from r2t2.core import add_reference

    @add_reference(
        short_purpose="Roasted chicken recipe", reference="Great British Roasts, 2019"
    )
    def roasted_chicken(ingredients=None):
        pass

    return roasted_chicken


class TestAddReference():
    def test_does_not_track_by_default(self, bibliography, chicken):
        assert "Great British Roasts, 2019" not in bibliography.references

    def test_does_not_track_by_default_when_called(self, bibliography, chicken):
        chicken()
        assert "Great British Roasts, 2019" not in bibliography.references

    def test_captures_when_tracking_on(self, bibliography, chicken):
        bibliography.tracking()
        chicken("Chicken")
        assert "Great British Roasts, 2019" in bibliography.references

        bibliography.tracking(False)

    def test_does_not_capture_when_not_called(self, bib_with_tracking, chicken):
        assert "Great British Roasts, 2019" not in bib_with_tracking

    def test_print_references(self, capsys, bib_with_tracking, chicken):
        chicken("Chicken")
        print(bib_with_tracking)
        captured = capsys.readouterr()

        assert "Great British Roasts, 2019" in captured.out
