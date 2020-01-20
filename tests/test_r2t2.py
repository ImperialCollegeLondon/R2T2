def decorated_function():
    from r2t2 import insert_reference

    @insert_reference(
        short_purpose="Roasted chicken recipe", reference="Great British Roasts, 2019"
    )
    def roasted_chicken(ingredients=None):
        pass

    return roasted_chicken


def test_print_references(capsys):
    from r2t2 import tracking, BIBLIOGRAPHY

    tracking()
    chicken = decorated_function()
    chicken("Chicken")
    print(BIBLIOGRAPHY)
    captured = capsys.readouterr()

    assert "Great British Roasts, 2019" in captured.out

    BIBLIOGRAPHY.clear()
    tracking(False)


def test_insert_reference():
    from r2t2 import tracking, BIBLIOGRAPHY

    chicken = decorated_function()
    assert "Great British Roasts, 2019" not in BIBLIOGRAPHY.references
    chicken()
    assert "Great British Roasts, 2019" not in BIBLIOGRAPHY.references

    tracking()
    chicken("Chicken")
    assert "Great British Roasts, 2019" in BIBLIOGRAPHY.references

    print(BIBLIOGRAPHY)

    BIBLIOGRAPHY.clear()
    tracking(False)
