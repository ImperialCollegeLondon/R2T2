from pathlib import Path

from r2t2.docstring_parser import (
    CodeDocumentComment,
    iter_extract_docstring_from_lines,
    iter_extract_docstring_from_file,
    iter_extract_docstring_from_files
)


DOC_STRING_LINE_1 = 'the docstring line 1'
DOC_STRING_LINE_2 = 'the docstring line 2'


class TestIterExtractDocstringFromLines:
    def test_should_extract_no_docstrings_from_empty_file(self):
        assert list(iter_extract_docstring_from_lines([])) == []

    def test_should_extract_no_docstrings_from_file_without_docstrings(self):
        assert list(iter_extract_docstring_from_lines([
            'def some_function():',
            '    pass'
        ])) == []

    def test_should_extract_module_level_docstring_using_double_quotes(self):
        assert list(iter_extract_docstring_from_lines([
            '"""',
            DOC_STRING_LINE_1,
            DOC_STRING_LINE_2,
            '"""'
        ])) == [CodeDocumentComment(
            name=None,
            lineno=1,
            text='\n'.join([
                DOC_STRING_LINE_1,
                DOC_STRING_LINE_2
            ])
        )]

    def test_should_extract_function_level_docstring_using_double_quotes(self):
        assert list(iter_extract_docstring_from_lines([
            'def some_function():',
            '    """',
            '    ' + DOC_STRING_LINE_1,
            '    ' + DOC_STRING_LINE_2,
            '    """',
            '    pass'
        ])) == [CodeDocumentComment(
            name='some_function',
            lineno=1,
            text='\n'.join([
                DOC_STRING_LINE_1,
                DOC_STRING_LINE_2
            ])
        )]


class TestIterExtractDocstringFromFile:
    def test_should_extract_module_level_docstring_using_double_quotes(
        self, temp_dir: Path
    ):
        file_path = temp_dir / 'test.py'
        file_path.write_text('\n'.join([
            '"""',
            DOC_STRING_LINE_1,
            DOC_STRING_LINE_2,
            '"""'
        ]))
        expected_docstrings = [CodeDocumentComment(
            filename=str(file_path),
            name=None,
            lineno=1,
            text='\n'.join([
                DOC_STRING_LINE_1,
                DOC_STRING_LINE_2
            ])
        )]
        assert list(iter_extract_docstring_from_file(
            str(file_path)
        )) == expected_docstrings
        assert list(iter_extract_docstring_from_file(
            Path(file_path)
        )) == expected_docstrings
        assert list(iter_extract_docstring_from_files(
            [str(file_path)]
        )) == expected_docstrings
