import ast
import logging
from pathlib import Path
from typing import Iterable, NamedTuple, Union, Optional


LOGGER = logging.getLogger(__name__)


DEFAULT_ENCODING = 'utf-8'


class CodeDocumentComment(NamedTuple):
    text: str
    filename: Optional[str] = None
    lineno: Optional[int] = None
    name: Optional[str] = None


def iter_extract_docstring_from_text(
    text: str, filename: str = None
) -> Iterable[CodeDocumentComment]:
    tree = ast.parse(text, filename=filename or '<unknown>')
    for node in ast.walk(tree):
        LOGGER.debug('node: %r', node)
        try:
            node_docstring = ast.get_docstring(node)
            LOGGER.debug('node_docstring: %r', node_docstring)
            if node_docstring:
                yield CodeDocumentComment(
                    filename=filename,
                    lineno=getattr(node, 'lineno', 1),
                    name=getattr(node, 'name', None),
                    text=node_docstring
                )
        except TypeError:
            # node type may not be able to have docstrings
            pass


def iter_extract_docstring_from_lines(
    lines: Iterable[str]
) -> Iterable[CodeDocumentComment]:
    return iter_extract_docstring_from_text('\n'.join(lines))


def iter_extract_docstring_from_file(
    path: Union[str, Path],
    encoding: str = DEFAULT_ENCODING
) -> Iterable[CodeDocumentComment]:
    return iter_extract_docstring_from_text(
        Path(path).read_text(encoding=encoding),
        filename=str(path)
    )


def iter_extract_docstring_from_files(
    paths: Iterable[Union[str, Path]],
    **kwargs
) -> Iterable[CodeDocumentComment]:
    for path in paths:
        yield from iter_extract_docstring_from_file(path, **kwargs)
