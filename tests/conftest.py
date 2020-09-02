import pytest


@pytest.fixture
def bibliography():
    from r2t2 import BIBLIOGRAPHY
    yield BIBLIOGRAPHY
    BIBLIOGRAPHY.clear()


@pytest.fixture
def bib_with_tracking(bibliography):
    bibliography.tracking()
    yield bibliography
    bibliography.tracking(False)
