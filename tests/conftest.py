import logging
from pathlib import Path

import pytest
from py._path.local import LocalPath

@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    for name in {'r2t2', 'tests'}:
        logging.getLogger(name).setLevel('DEBUG')


@pytest.fixture()
def temp_dir(tmpdir: LocalPath) -> Path:
    # maps the pytest "tmpdir" fixture to a regular pathlib Path type
    return Path(tmpdir)
