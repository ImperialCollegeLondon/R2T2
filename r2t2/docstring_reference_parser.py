import logging
import os
from pathlib import Path
from typing import Iterable, List, Tuple, Union

from r2t2.core import Biblio, BIBLIOGRAPHY, FunctionReference
from r2t2.plain_text_parser import iter_parse_plain_text_references
from r2t2.docstring_parser import (
    CodeDocumentComment,
    iter_extract_docstring_from_files
)


LOGGER = logging.getLogger(__name__)


DOCSTRING_SHORT_PURPOSE = 'automatically parsed from docstring'


def expand_file_list(path: Union[Path, str]) -> List[Path]:
    if os.path.isdir(path):
        return sorted(Path(path).rglob("*.py"))
    else:
        return [Path(path)]


def get_function_reference_identifier(function_reference: FunctionReference) -> str:
    return "{source}:{line_num}".format(
        source=function_reference.source,
        line_num=function_reference.line
    )


def get_function_reference_from_docstring(
    docstring: CodeDocumentComment
) -> FunctionReference:
    references = list(iter_parse_plain_text_references(docstring.text))
    return FunctionReference(
        source=docstring.filename or '',
        line=docstring.lineno or 0,
        name=docstring.name or '',
        references=references,
        short_purpose=[DOCSTRING_SHORT_PURPOSE] * len(references)
    )


def iter_parse_docstring_function_references_from_files(
    filenames: Iterable[Union[str, Path]]
) -> Iterable[Tuple[str, FunctionReference]]:
    for docstring in iter_extract_docstring_from_files(filenames):
        function_reference = get_function_reference_from_docstring(docstring)
        identifier = get_function_reference_identifier(function_reference)
        yield identifier, function_reference


def parse_and_add_docstring_references_from_files(
    filenames: Iterable[Union[str, Path]],
    biblio: Biblio = None
):
    if biblio is None:
        biblio = BIBLIOGRAPHY
    biblio.update(dict(
        iter_parse_docstring_function_references_from_files(filenames)
    ))
