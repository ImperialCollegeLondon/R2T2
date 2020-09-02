import logging
from pathlib import Path

from pytest import fixture
from py._path.local import LocalPath


@fixture
def decorated_function():
    from r2t2 import add_reference

    @add_reference(
        short_purpose="Roasted chicken recipe", reference="Great British Roasts, 2019"
    )
    def roasted_chicken(ingredients=None):
        pass

    return roasted_chicken


@fixture
def decorated_with_doi():
    from r2t2 import add_reference

    @add_reference(short_purpose="DOI reference", doi="10.5281/zenodo.1185316")
    def a_great_function():
        pass

    return a_great_function


@fixture(scope='session', autouse=True)
def setup_logging():
    for name in {'r2t2', 'tests'}:
        logging.getLogger(name).setLevel('DEBUG')


@fixture()
def temp_dir(tmpdir: LocalPath) -> Path:
    # maps the pytest "tmpdir" fixture to a regular pathlib Path type
    return Path(tmpdir)
