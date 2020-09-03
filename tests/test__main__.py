import pytest

from r2t2.__main__ import (
    parse_args,
    main
)


VALID_FORMAT = 'markdown'
INVALID_FORMAT = 'other'


class TestParseArgs:
    def test_should_not_fail_on_valid_format(self):
        args = parse_args([
            '--format=%s' % VALID_FORMAT,
            'docs/examples'
        ])
        assert args.format == VALID_FORMAT

    def test_should_fail_on_invalid_format(self):
        with pytest.raises(SystemExit):
            parse_args([
                '--format=%s' % INVALID_FORMAT,
                'docs/examples'
            ])


@pytest.mark.usefixtures('bibliography')
class TestMain:
    def test_should_not_fail_on_static_analysis_of_examples_including_docstrings(
        self
    ):
        main([
            '--static',
            '--docstring',
            'docs/examples'
        ])

    def test_should_not_fail_on_static_analysis_of_examples_ignoring_docstrings(
        self
    ):
        main([
            '--static',
            'docs/examples'
        ])

    def test_should_not_fail_on_runtime_analysis_of_examples(self):
        main([
            'docs/examples'
        ])
