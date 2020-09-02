import pytest

from r2t2.core import add_reference


@pytest.fixture
def chicken():
    @add_reference(
        short_purpose="Roasted chicken recipe", reference="Great British Roasts, 2019"
    )
    def roasted_chicken(ingredients=None):
        pass

    return roasted_chicken


class TestAddReference():
    def test_does_not_track_by_default(self, bibliography, chicken):
        assert len(bibliography.references) == 0
        assert "Great British Roasts, 2019" not in bibliography.references

    def test_does_not_track_by_default_when_called(self, bibliography, chicken):
        chicken()
        assert len(bibliography.references) == 0
        assert "Great British Roasts, 2019" not in bibliography.references

    def test_captures_when_tracking_on(self, bibliography, chicken):
        bibliography.tracking()
        chicken("Chicken")
        assert len(bibliography.references) == 1
        assert "Great British Roasts, 2019" in bibliography.references

        bibliography.tracking(False)

    def test_clear_removes_everything(self, bib_with_tracking, chicken):
        assert len(bib_with_tracking) == 0
        assert len(bib_with_tracking.references) == 0
        chicken()
        bib_with_tracking.clear()
        assert len(bib_with_tracking) == 0
        assert len(bib_with_tracking.references) == 0

    def test_does_not_capture_when_not_called(self, bib_with_tracking, chicken):
        assert "Great British Roasts, 2019" not in bib_with_tracking

    def test_works_with_two_functions(self, bib_with_tracking):
        @add_reference(short_purpose="Function 1", reference="Reference 1")
        def my_func_1():
            pass

        @add_reference(short_purpose="Function 2", reference="Reference 2")
        def my_func_2():
            pass

        my_func_1()
        my_func_2()

        assert len(bib_with_tracking) == 2
        assert len(bib_with_tracking.references) == 2

    def test_captures_multiple_refs(self, bib_with_tracking):
        @add_reference(short_purpose="testing", reference="Reference 1")
        @add_reference(short_purpose="testing", reference="Reference 2")
        def my_func_1():
            pass
        my_func_1()

        assert "Reference 1" in bib_with_tracking.references
        assert "Reference 2" in bib_with_tracking.references
        assert len(bib_with_tracking.references) == 2

    def test_ignores_duplicate_ref(self, bib_with_tracking):
        @add_reference(short_purpose="testing", reference="Reference 1")
        @add_reference(short_purpose="testing", reference="Reference 1")
        def my_func_2():
            pass
        my_func_2()

        assert "Reference 1" in bib_with_tracking.references
        assert len(bib_with_tracking.references) == 1

    def test_print_references(self, capsys, bib_with_tracking, chicken):
        chicken("Chicken")
        print(bib_with_tracking)
        captured = capsys.readouterr()

        assert "Great British Roasts, 2019" in captured.out
