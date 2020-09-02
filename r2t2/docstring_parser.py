import ast
import logging

from typing import Iterable


LOGGER = logging.getLogger(__name__)


def iter_extract_docstring_from_lines(lines: Iterable[str]) -> Iterable[str]:
    current_docstring_lines = []
    tree = ast.parse('\n'.join(lines))
    for node in ast.walk(tree):
        LOGGER.debug('node: %r', node)
        try:
            node_docstring = ast.get_docstring(node)
            LOGGER.debug('node_docstring: %r', node_docstring)
            if node_docstring:
                yield str(node_docstring)
        except TypeError:
            # node type may not be able to have docstrings
            pass
