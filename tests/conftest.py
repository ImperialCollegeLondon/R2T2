import logging
from pathlib import Path

import pytest
from py._path.local import LocalPath


@pytest.fixture
def bibliography():
    from r2t2 import BIBLIOGRAPHY

    BIBLIOGRAPHY.tracking(False)
    yield BIBLIOGRAPHY
    BIBLIOGRAPHY.clear()


@pytest.fixture
def bib_with_tracking(bibliography):
    bibliography.tracking()
    yield bibliography
    bibliography.tracking(False)


@pytest.fixture
def decorated_function():
    from r2t2 import add_reference

    @add_reference(
        short_purpose="Roasted chicken recipe", reference="Great British Roasts, 2019"
    )
    def roasted_chicken(ingredients=None):
        pass

    return roasted_chicken


@pytest.fixture
def decorated_with_doi():
    from r2t2 import add_reference

    @add_reference(short_purpose="DOI reference", doi="10.5281/zenodo.1185316")
    def a_great_function():
        pass

    return a_great_function


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    for name in {"r2t2", "tests"}:
        logging.getLogger(name).setLevel("DEBUG")


@pytest.fixture()
def temp_dir(tmpdir: LocalPath) -> Path:
    # maps the pytest "tmpdir" fixture to a regular pathlib Path type
    return Path(tmpdir)
