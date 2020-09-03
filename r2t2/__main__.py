import argparse
import logging
import os
from pathlib import Path
from typing import List

from .static_parser import locate_references
from .runtime_tracker import runtime_tracker
from .writers import REGISTERED_WRITERS
from .docstring_reference_parser import (
    expand_file_list,
    parse_and_add_docstring_references_from_files
)


def parse_args(argv: List[str] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f",
        "--format",
        default="terminal",
        type=str,
        choices=sorted(REGISTERED_WRITERS.keys()),
        help="Format of the output. Default: Terminal."
    )

    parser.add_argument(
        "-o",
        "--output",
        default=None,
        type=str,
        help="File to save the references into. Ignored if format is 'Terminal'."
        " Default: [target folder]/references.",
    )

    parser.add_argument(
        "-s",
        "--static",
        action="store_true",
        help="When processing a file, indicates if a static analysis"
        " should be done rather than a runtime analysis, "
        " the default behaviour for files.",
    )

    parser.add_argument(
        "--notebook",
        action="store_true",
        help="Parse markdown cells from Jupyter notebooks.",
    )

    parser.add_argument(
        "--docstring",
        action="store_true",
        help="Also parse docstrings.",
    )

    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="The encoding to use when parsing files.",
    )

    parser.add_argument(
        "target",
        default=".",
        nargs="?",
        type=str,
        help="Target file or folder to analyse. If the target is a python file,"
        " this is run as a script and the references provided are those"
        " found at runtime."
        " Default: Current directory.",
    )

    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Input arguments for running the target script, if needed.",
    )

    args = parser.parse_args(argv)
    return args


def run(args: argparse.Namespace):
    if args.output is None:
        if os.path.isdir(args.target):
            output = Path(args.target) / "references"
        else:
            output = Path(args.target).parent / "references"
    elif os.path.isdir(args.output):
        msg = f"Output must be file, not a directory. Now it is {args.output}"
        raise IsADirectoryError(msg)
    else:
        output = Path(args.output)

    if os.path.isdir(args.target) or args.static:
        locate_references(args.target, encoding=args.encoding)
        if args.notebook:
            if not args.target.endswith('.ipynb'):
                raise Exception("If --notebook flag is passed, target must be a"
                                " Jupyter notebook!")
        if args.docstring:
            if not args.target.endswith('.py'):
                raise Exception("If --docstring flag is passed, target must be a"
                                " python script!")
        if args.docstring or args.notebook:
            parse_and_add_docstring_references_from_files(
                expand_file_list(args.target),
                encoding=args.encoding,
            )
        if args.docstring:
            parse_and_add_docstring_references_from_files(
                expand_file_list(args.target),
                encoding=args.encoding
            )
    else:
        runtime_tracker(args.target, args.args)

    REGISTERED_WRITERS[args.format](output)


def main(argv: List[str] = None):
    args = parse_args(argv)
    run(args)


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    main()
