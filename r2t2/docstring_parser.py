import ast
import logging
import json
from pathlib import Path
from typing import Iterable, NamedTuple, Union, Optional


LOGGER = logging.getLogger(__name__)
FAKE_FUNC = """def cell_{}():
    \"\"\"
    {}
    \"\"\"
"""


class CodeDocumentComment(NamedTuple):
    text: str
    filename: Optional[str] = None
    lineno: Optional[int] = None
    name: Optional[str] = None


def iter_extract_docstring_from_text(
    text: str, filename: str = None,
    notebook: bool = False,
) -> Iterable[CodeDocumentComment]:
    tree = ast.parse(text, filename=filename or '<unknown>')
    for node in ast.walk(tree):
        LOGGER.debug('node: %r', node)
        try:
            node_docstring = ast.get_docstring(node)
            LOGGER.debug('node_docstring: %r', node_docstring)
            if node_docstring:
                if notebook:
                    lineno = 'n/a'
                else:
                    lineno = getattr(node, 'lineno', 1)
                yield CodeDocumentComment(
                    filename=filename,
                    lineno=lineno,
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
    path: Union[str, Path]
) -> Iterable[CodeDocumentComment]:
    path = Path(path)
    txt = path.read_text(encoding='utf-8')
    notebook = False
    if path.suffix == ".ipynb":
        cells = json.loads(txt)["cells"]
        txt = []
        # extract the markdown text from all markdown cells, and make each of
        # them look like the docstring of a separate function
        for i, c in enumerate(cells):
            if c["cell_type"] == "markdown":
                txt.append(FAKE_FUNC.format(i, "    ".join(c["source"])))
        txt = "\n".join(txt)
        notebook = True
    return iter_extract_docstring_from_text(txt, filename=str(path),
                                            notebook=notebook)


def iter_extract_docstring_from_files(
    paths: Iterable[Union[str, Path]]
) -> Iterable[CodeDocumentComment]:
    for path in paths:
        yield from iter_extract_docstring_from_file(path)
