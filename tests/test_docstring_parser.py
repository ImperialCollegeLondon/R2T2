from r2t2.docstring_parser import iter_extract_docstring_from_lines


DOC_STRING_LINE_1 = 'the docstring line 1'
DOC_STRING_LINE_2 = 'the docstring line 2'


class TestIterExtractDocstringFromLines:
    def _test_should_extract_no_docstrings_from_empty_file(self):
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
        ])) == ['\n'.join([
            DOC_STRING_LINE_1,
            DOC_STRING_LINE_2
        ])]

    def test_should_extract_function_level_docstring_using_double_quotes(self):
        assert list(iter_extract_docstring_from_lines([
            'def some_function():',
            '    """',
            '    ' + DOC_STRING_LINE_1,
            '    ' + DOC_STRING_LINE_2,
            '    """',
            '    pass'
        ])) == ['\n'.join([
            DOC_STRING_LINE_1,
            DOC_STRING_LINE_2
        ])]
