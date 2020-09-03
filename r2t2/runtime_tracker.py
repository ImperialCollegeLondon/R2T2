import logging
import sys
import os
from typing import List

from .core import BIBLIOGRAPHY


LOGGER = logging.getLogger(__name__)


def runtime_tracker(script: str, args: List[str], encoding: str):
    BIBLIOGRAPHY.tracking()

    sys.argv = [script, *args]
    sys.path[0] = os.path.dirname(script)

    try:
        LOGGER.debug(
            "loading script: %s (args: %s, encoding: %s)", script, args, encoding
        )
        with open(script, encoding=encoding) as fp:
            code = compile(fp.read(), script, "exec")

        # try to emulate __main__ namespace as much as possible
        # What trace python module uses https://docs.python.org/3.7/library/trace.html
        globs = {
            "__file__": script,
            "__name__": "__main__",
            "__package__": None,
            "__cached__": None,
        }
        exec(code, globs, globs)

    except OSError as err:
        sys.exit("Cannot run file %r because: %s" % (sys.argv[0], err))

    except SystemExit:
        pass
