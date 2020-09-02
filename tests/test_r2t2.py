def decorated_function():
    from r2t2 import add_reference

    @add_reference(
        short_purpose="Roasted chicken recipe", reference="Great British Roasts, 2019"
    )
    def roasted_chicken(ingredients=None):
        pass

    return roasted_chicken


def test_add_reference_no_tracking(bibliography):
    chicken = decorated_function()
    assert "Great British Roasts, 2019" not in bibliography.references
    chicken()
    assert "Great British Roasts, 2019" not in bibliography.references


def test_add_reference_with_tracking(bibliography):
    chicken = decorated_function()
    bibliography.tracking()
    chicken("Chicken")
    assert "Great British Roasts, 2019" in bibliography.references

    bibliography.tracking(False)


def test_print_references(capsys, bib_with_tracking):
    chicken = decorated_function()
    chicken("Chicken")
    print(bib_with_tracking)
    captured = capsys.readouterr()

    assert "Great British Roasts, 2019" in captured.out
