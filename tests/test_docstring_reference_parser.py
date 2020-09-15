from pathlib import Path

from r2t2.core import Biblio, FunctionReference
from r2t2.docstring_reference_parser import (
    DOCSTRING_SHORT_PURPOSE,
    NOTEBOOK_SHORT_PURPOSE,
    parse_and_add_docstring_references_from_files
)

DOI_URL_HTTPS_PREFIX = 'https://doi.org/'
HERE = Path(__file__).parent
FIXTURES = HERE / "fixtures"

DOI_1 = '10.1234/zenodo.1234567'
DOI_2 = '10.5281/zenodo.1185316'
DOI_3 = '10.3435/zenodo.1579823'


class TestParseAndAddDocstringReferencesFromFiles:
    def test_should_parse_docstring_reference(
        self, temp_dir: Path
    ):
        file_path = temp_dir / 'test.py'
        file_path.write_text('\n'.join([
            'def some_function():'
            '    """',
            '    ' + DOI_1,
            '    """'
        ]))
        biblio = Biblio()
        parse_and_add_docstring_references_from_files(
            [file_path],
            biblio=biblio
        )
        expected_identifier = '{source}:{name}:{line_num}'.format(
            source=str(file_path),
            name='some_function',
            line_num=1,
        )
        assert biblio.keys() == {expected_identifier}
        function_reference = biblio[expected_identifier]
        assert function_reference.name == 'some_function'
        assert function_reference.source == str(file_path)
        assert function_reference.line == 1
        assert function_reference.references == [DOI_URL_HTTPS_PREFIX + DOI_1]
        assert function_reference.short_purpose == [DOCSTRING_SHORT_PURPOSE]

    def test_should_not_override_existing_reference(
        self, temp_dir: Path
    ):
        file_path = temp_dir / 'test.py'
        file_path.write_text('\n'.join([
            'def some_function():'
            '    """',
            '    ' + DOI_1,
            '    """'
        ]))
        expected_identifier = '{source}:{name}:{line_num}'.format(
            source=str(file_path),
            name='some_function',
            line_num=1,
        )
        biblio = Biblio()
        existing_function_reference = FunctionReference(
            name='other',
            source='other.py',
            line=-1,
            short_purpose=['For testing'],
            references=['test/123']
        )
        biblio[expected_identifier] = existing_function_reference
        parse_and_add_docstring_references_from_files(
            [file_path],
            biblio=biblio
        )
        assert biblio == {expected_identifier: existing_function_reference}

    def test_should_not_add_function_reference_without_references(
        self, temp_dir: Path
    ):
        file_path = temp_dir / 'test.py'
        file_path.write_text('\n'.join([
            'def some_function():'
            '    """',
            '    some docstring',
            '    """'
        ]))
        biblio = Biblio()
        parse_and_add_docstring_references_from_files(
            [file_path],
            biblio=biblio
        )
        assert not biblio

    def test_should_parse_notebook_references(
        self
    ):
        file_path = FIXTURES / "notebook_doi.ipynb"
        biblio = Biblio()
        parse_and_add_docstring_references_from_files(
            [file_path],
            biblio=biblio
        )
        identifiers = '{source}:{name}:{line_num}'
        names = ['cell_0', 'cell_4']
        dois = [[DOI_2, DOI_3], [DOI_1]]
        expected_identifiers = [
            identifiers.format(
                source=str(file_path),
                name=names[0],
                line_num="n/a",
            ),
            identifiers.format(
                source=str(file_path),
                name=names[1],
                line_num="n/a",
            ),
        ]
        assert biblio.keys() == set(expected_identifiers)
        for i, identifier in enumerate(expected_identifiers):
            function_reference = biblio[identifier]
            assert function_reference.name == names[i]
            assert function_reference.source == str(file_path)
            assert function_reference.line is None
            assert function_reference.references == [DOI_URL_HTTPS_PREFIX + d
                                                     for d in dois[i]]
            assert function_reference.short_purpose == ([NOTEBOOK_SHORT_PURPOSE]
                                                        * len(dois[i]))
