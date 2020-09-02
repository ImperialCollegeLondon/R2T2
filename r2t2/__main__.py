import argparse
import os
import sys
from pathlib import Path

from .static_parser import locate_references
from .runtime_tracker import runtime_tracker
from .writers import REGISTERED_WRITERS
from .reference_processors import PROCESSORS

parser = argparse.ArgumentParser()

parser.add_argument(
    "-f",
    "--format",
    default="terminal",
    type=str,
    help=f"Format of the output. Default: Terminal. "
    f"Valid options are: {','.join(list(REGISTERED_WRITERS.keys()))}.",
)

parser.add_argument(
    "-o",
    "--output",
    default=None,
    type=str,
    help="File to save the references into. Ignored if format is 'Terminal'."
    "Default: [target folder]/references.",
)

parser.add_argument(
    "-s",
    "--static",
    action="store_true",
    help="When processing a file, indicates if a static analysis should be done rather "
    "than a runtime analysis, the default behaviour for files.",
)

parser.add_argument(
    "-p",
    "--processor",
    default="plain",
    type=str,
    help=f"Processor(s) for references. Default: plain. "
    "Multiple processors can be used and should be passed as a comma-separated list."
    f"Valid options are: {','.join(list(PROCESSORS.keys()))}.",
)

parser.add_argument(
    "-b",
    "--bibtex",
    type=str,
    help="Bibtex file for processing references with bibtex.",
)

parser.add_argument(
    "target",
    default=".",
    nargs="?",
    type=str,
    help="Target file or folder to analyse. If the target is a python file, this is "
    "run as a script and the references provided are those found at runtime. "
    "Default: Current directory.",
)

parser.add_argument(
    "args",
    nargs=argparse.REMAINDER,
    help="Input arguments for running the target script, if needed.",
)

args = parser.parse_args()

if args.format not in REGISTERED_WRITERS:
    print(
        f"ERROR: Unrecognized output formats. "
        f"Valid options for -f are: {', '.join(list(REGISTERED_WRITERS.keys()))}"
    )
    sys.exit()

if args.processor is not None and args.processor not in PROCESSORS:
    print(
        f"ERROR: Unrecognized processor format '{args.processor}'. "
        f"Valid options for -p are: {', '.join(list(PROCESSORS.keys()))}"
    )
    sys.exit()
else:
    processors = args.processor.split(",")

if "bibtex" in args.processor.split(",") and args.bibtex is None:
    print(
        "ERROR: Bibtex processor format selected but no file given. "
        "Please provide a .bib file with the --bibtex (-b) argument."
    )
    processor_source = None  # TODO a better way to handle this?
    sys.exit()
else:
    processor_source = args.bibtex

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
    locate_references(args.target)
else:
    runtime_tracker(args.target, args.args)

# TODO how to pass to processor(s) with processor_source for bibtex?
REGISTERED_WRITERS[args.format](output)
