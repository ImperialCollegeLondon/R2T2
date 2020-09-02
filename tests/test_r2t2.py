def decorated_function():
    from r2t2 import add_reference

    @add_reference(
        short_purpose="Roasted chicken recipe", reference="Great British Roasts, 2019"
    )
    def roasted_chicken(ingredients=None):
        pass

    return roasted_chicken


def test_add_reference():
    from r2t2 import BIBLIOGRAPHY

    chicken = decorated_function()
    assert "Great British Roasts, 2019" not in BIBLIOGRAPHY.references
    chicken()
    assert "Great British Roasts, 2019" not in BIBLIOGRAPHY.references

    BIBLIOGRAPHY.tracking()
    chicken("Chicken")
    assert "Great British Roasts, 2019" in BIBLIOGRAPHY.references

    BIBLIOGRAPHY.clear()
    BIBLIOGRAPHY.tracking(False)


def test_print_references(capsys):
    from r2t2 import BIBLIOGRAPHY

    BIBLIOGRAPHY.tracking()
    chicken = decorated_function()
    chicken("Chicken")
    print(BIBLIOGRAPHY)
    captured = capsys.readouterr()

    assert "Great British Roasts, 2019" in captured.out

    BIBLIOGRAPHY.clear()
    BIBLIOGRAPHY.tracking(False)
