def test_add_reference(decorated_function):
    from r2t2 import BIBLIOGRAPHY

    assert "[plain]Great British Roasts, 2019" not in BIBLIOGRAPHY.references
    decorated_function()
    assert "[plain]Great British Roasts, 2019" not in BIBLIOGRAPHY.references

    BIBLIOGRAPHY.tracking()
    decorated_function("Chicken")
    assert "[plain]Great British Roasts, 2019" in BIBLIOGRAPHY.references

    BIBLIOGRAPHY.clear()
    BIBLIOGRAPHY.tracking(False)


def test_print_references(capsys, decorated_function):
    from r2t2 import BIBLIOGRAPHY

    BIBLIOGRAPHY.tracking()
    decorated_function("Chicken")
    print(BIBLIOGRAPHY)
    captured = capsys.readouterr()

    assert "Great British Roasts, 2019" in captured.out

    BIBLIOGRAPHY.clear()
    BIBLIOGRAPHY.tracking(False)


def test_add_reference_from_doi(decorated_with_doi):
    from r2t2 import BIBLIOGRAPHY

    BIBLIOGRAPHY.tracking()

    decorated_with_doi()
    assert "[doi]https://doi.org/" in BIBLIOGRAPHY.references[-1]

    BIBLIOGRAPHY.clear()
    BIBLIOGRAPHY.tracking(False)
