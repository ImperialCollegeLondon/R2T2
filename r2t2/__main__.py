import argparse
import os
from pathlib import Path

from .static_tracker import locate_references, to_markdown
from .runtime_tracker import runtime_tracker

parser = argparse.ArgumentParser()

parser.add_argument(
    "-o",
    "--output",
    default=None,
    type=str,
    help="File to save the references into. Default: [target folder]/references.md.",
)

parser.add_argument(
    "-s",
    "--static",
    action="store_true",
    help="When processing a file, indicates if a static analysis should be done rather "
    "than a runtime analysis, the default behaviour for files.",
)

parser.add_argument(
    "target",
    default=".",
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

if args.output is None:
    if os.path.isdir(args.target):
        output = Path(args.target) / "references.md"
    else:
        output = Path(args.target).parent / "references.md"
elif os.path.isdir(args.output):
    msg = f"Output must be file, not a directory. Now it is {args.output}"
    raise IsADirectoryError(msg)
else:
    output = Path(args.output)

if os.path.isdir(args.target) or args.static:
    to_markdown(locate_references(args.target), output)
else:
    runtime_tracker(args.target, args.args)
