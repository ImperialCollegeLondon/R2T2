import ast
import logging
from pathlib import Path
from typing import Iterable, Union


LOGGER = logging.getLogger(__name__)


def iter_extract_docstring_from_text(text: str) -> Iterable[str]:
    tree = ast.parse(text)
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


def iter_extract_docstring_from_lines(lines: Iterable[str]) -> Iterable[str]:
    return iter_extract_docstring_from_text('\n'.join(lines))


def iter_extract_docstring_from_file(path: Union[str, Path]) -> Iterable[str]:
    return iter_extract_docstring_from_text(Path(path).read_text())


def iter_extract_docstring_from_files(paths: Iterable[Union[str, Path]]) -> Iterable[str]:
    for path in paths:
        yield from iter_extract_docstring_from_file(path)
