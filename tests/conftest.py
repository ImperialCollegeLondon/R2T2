import logging
import pytest


@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    for name in {'r2t2', 'tests'}:
        logging.getLogger(name).setLevel('DEBUG')
