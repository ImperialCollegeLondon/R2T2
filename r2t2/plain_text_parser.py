import re

from typing import Iterable, List


DOI_URL_HTTPS_PREFIX = 'https://doi.org/'


def iter_doi(text: str) -> Iterable[str]:
    for m in re.findall(r'\b10\.\d{4,}/\S+', text):
        yield DOI_URL_HTTPS_PREFIX + str(m)


def iter_latex_reference_names(text: str) -> Iterable[str]:
    for m in re.finditer(r'\\cite{([^}]+)}', text):
        yield m.group(1)


def iter_parse_plain_text_references(text: str) -> Iterable[str]:
    yield from iter_doi(text)
    yield from iter_latex_reference_names(text)


def parse_plain_text_references(text: str) -> List[str]:
    return list(iter_parse_plain_text_references(text))
