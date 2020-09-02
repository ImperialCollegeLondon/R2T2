from r2t2.plain_text_parser import (
    parse_plain_text_references
)


DOI_URL_HTTP_PREFIX = 'http://doi.org/'
DOI_URL_HTTPS_PREFIX = 'https://doi.org/'

DOI_1 = '10.1234/zenodo.1234567'


class TestParsePlainTextReferences:
    def test_should_return_empty_list_for_empty_string(self):
        assert parse_plain_text_references('') == []

    def test_should_return_empty_list_for_text_without_reference(self):
        assert parse_plain_text_references('description of some function') == []

    def test_should_parse_doi_without_additional_text(self):
        assert parse_plain_text_references(
            DOI_1
        ) == [DOI_1]

    def test_should_parse_doi_with_surround_text(self):
        assert parse_plain_text_references(
            'DOI: ' + DOI_1 + ' used for xyz'
        ) == [DOI_1]

    def test_should_parse_doi_http_url(self):
        assert parse_plain_text_references(
            DOI_URL_HTTP_PREFIX + DOI_1
        ) == [DOI_1]

    def test_should_parse_doi_https_url(self):
        assert parse_plain_text_references(
            DOI_URL_HTTP_PREFIX + DOI_1
        ) == [DOI_1]
