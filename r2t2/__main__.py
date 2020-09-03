import argparse
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

from .static_parser import locate_references
from .runtime_tracker import runtime_tracker
from .writers import REGISTERED_WRITERS
from .docstring_reference_parser import (
    expand_file_list,
    parse_and_add_docstring_references_from_files
)


LOGGER = logging.getLogger(__name__)


class SubCommand(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    @abstractmethod
    def run(self, args: argparse.Namespace):
        pass


def add_common_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-f",
        "--format",
        default="terminal",
        type=str,
        choices=sorted(REGISTERED_WRITERS.keys()),
        help="Format of the output. Default: Terminal."
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="The encoding to use when parsing files.",
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
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )


class RunSubCommand(SubCommand):
    def __init__(self):
        super().__init__("run", "Run script and use runtime tracking")

    def add_arguments(self, parser: argparse.ArgumentParser):
        add_common_arguments(parser)
        parser.add_argument(
            "target",
            type=str,
            help="This is run as a script and the references provided are those"
            " found at runtime.",
        )
        parser.add_argument(
            "args",
            nargs=argparse.REMAINDER,
            help="Input arguments for running the target script, if needed.",
        )

    def run(self, args: argparse.Namespace):
        runtime_tracker(args.target, args.args, encoding=args.encoding)


class StaticSubCommand(SubCommand):
    def __init__(self):
        super().__init__("static", "Run static analysis")

    def add_arguments(self, parser: argparse.ArgumentParser):
        add_common_arguments(parser)
        parser.add_argument(
            "--docstring",
            action="store_true",
            help="Also parse docstrings.",
        )
        parser.add_argument(
            "--notebook",
            action="store_true",
            help="Parse markdown cells from Jupyter notebooks.",
        )
        parser.add_argument(
            "target",
            default=".",
            type=str,
            help="Target file or folder to analyse."
            " Default: Current directory.",
        )

    def run(self, args: argparse.Namespace):
        if args.notebook:
            if not args.target.endswith('.ipynb'):
                raise Exception("If --notebook flag is passed, target must be a"
                                " Jupyter notebook!")
        locate_references(args.target, encoding=args.encoding)
        if args.docstring or args.notebook:
            parse_and_add_docstring_references_from_files(
                expand_file_list(args.target),
                encoding=args.encoding
            )


SUB_COMMANDS: List[SubCommand] = [
    RunSubCommand(),
    StaticSubCommand()
]

SUB_COMMAND_BY_NAME: Dict[str, SubCommand] = {
    sub_command.name: sub_command for sub_command in SUB_COMMANDS
}


def parse_args(argv: List[str] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True
    for sub_command in SUB_COMMANDS:
        sub_parser = subparsers.add_parser(
            sub_command.name, help=sub_command.description
        )
        sub_command.add_arguments(sub_parser)

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

    sub_command = SUB_COMMAND_BY_NAME[args.command]
    sub_command.run(args)

    REGISTERED_WRITERS[args.format](output)


def main(argv: List[str] = None):
    args = parse_args(argv)
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    LOGGER.debug("args: %s", args)
    run(args)


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    main()
