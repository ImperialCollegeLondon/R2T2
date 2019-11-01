import argparse
import os

from .static_tracker import locate_references, to_markdown

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--input",
    default=".",
    type=str,
    help="Target file or folder to analyse. Default: Current directory.",
)
parser.add_argument(
    "-o",
    "--output",
    default="references.md",
    type=str,
    help="File to save the references into. Default: references.md.",
)

args = parser.parse_args()

if os.path.isdir(args.output):
    msg = f"Output must be file, not a directly. Now it is {args.output}"
    raise IsADirectoryError(msg)

to_markdown(locate_references(args.input), args.output)
