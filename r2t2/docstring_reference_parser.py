import logging
import os
from pathlib import Path
from typing import Iterable, List, Tuple, Union

from r2t2.core import Biblio, BIBLIOGRAPHY, FunctionReference
from r2t2.docstring_parser import iter_extract_docstring_from_files
from r2t2.plain_text_parser import iter_parse_plain_text_references


LOGGER = logging.getLogger(__name__)


def expand_file_list(path: Union[Path, str]) -> List[Path]:
    if os.path.isdir(path):
        return sorted(Path(path).rglob("*.py"))
    else:
        return [Path(path)]


def get_function_reference_from_docstring(docstring: str) -> FunctionReference:
    return FunctionReference(
        name='todo',
        source='todo.py',
        line=1,
        references=list(iter_parse_plain_text_references(docstring))
    )


def iter_parse_docstring_function_references_from_files(
    filenames: Iterable[Union[str, Path]]
) -> Iterable[Tuple[str, FunctionReference]]:
    for i, docstring in enumerate(iter_extract_docstring_from_files(filenames)):
        yield str(i), get_function_reference_from_docstring(docstring)


def parse_and_add_docstring_references_from_files(
    filenames: Iterable[Union[str, Path]],
    biblio: Biblio = None
):
    if biblio is None:
        biblio = BIBLIOGRAPHY
    biblio.update(dict(
        iter_parse_docstring_function_references_from_files(filenames)
    ))
