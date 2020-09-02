from r2t2.core import add_reference


class TestAddReference():
    def test_does_not_track_by_default(self, bibliography, decorated_function):
        assert len(bibliography.references) == 0
        assert "Great British Roasts, 2019" not in bibliography.references

    def test_does_not_track_by_default_when_called(self, bibliography, decorated_function):
        decorated_function()
        assert len(bibliography.references) == 0
        assert "Great British Roasts, 2019" not in bibliography.references

    def test_captures_when_tracking_on(self, bibliography, decorated_function):
        bibliography.tracking()
        decorated_function("Chicken")
        assert len(bibliography.references) == 1
        assert "Great British Roasts, 2019" in bibliography.references

        bibliography.tracking(False)

    def test_clear_removes_everything(self, bib_with_tracking, decorated_function):
        assert len(bib_with_tracking) == 0
        assert len(bib_with_tracking.references) == 0
        decorated_function()
        bib_with_tracking.clear()
        assert len(bib_with_tracking) == 0
        assert len(bib_with_tracking.references) == 0

    def test_does_not_capture_when_not_called(self, bib_with_tracking, decorated_function):
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

    def test_print_references(self, capsys, bib_with_tracking, decorated_function):
        decorated_function("Chicken")
        print(bib_with_tracking)
        captured = capsys.readouterr()

        assert "Great British Roasts, 2019" in captured.out

    def test_add_reference_from_doi(self, decorated_with_doi):
        from r2t2 import BIBLIOGRAPHY

        BIBLIOGRAPHY.tracking()

        decorated_with_doi()
        assert "https://doi.org/" in BIBLIOGRAPHY.references[-1]

        BIBLIOGRAPHY.clear()
        BIBLIOGRAPHY.tracking(False)
