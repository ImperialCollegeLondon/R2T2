from pathlib import Path
import re
from typing import Union, List
import os
from functools import reduce

from .core import BIBLIOGRAPHY, FunctionReference


def locate_references(path: Union[Path, str]):
    """Locates add_reference in path.

    It looks recursively for add_reference markers, taking note of the module, line
    short_purpose and actual reference string.

    Returns
        None
    """
    if os.path.isdir(path):
        filenames = sorted(Path(path).rglob("*.py"))
    else:
        filenames = [Path(path)]

    ref_located = False
    ref_lines = []
    code_str = []
    for filename in filenames:
        with open(filename, "r") as f:
            for num, line in enumerate(f):
                if line.strip().startswith("@add_reference"):
                    ref_located = True
                    ref_lines.append(num)
                    code_str.append(line.strip())
                    continue

                if ref_located and (
                    line.strip().startswith("def ") or line.strip().startswith("class ")
                ):
                    ref_lines.append(num)
                    ref_lines = [r - ref_lines[0] for r in ref_lines]
                    parse_references(str(filename), line, num + 1, code_str, ref_lines)
                    ref_located = False
                    ref_lines = []
                    code_str = []

                elif ref_located:
                    code_str.append(line.strip())


def _add_reference(**kwargs):
    return kwargs


def parse_references(
    source: str, current: str, line_num: int, ref_raw: List[str], ref_lines: List[int]
):
    """Extracts all references added to a function or class."""
    name = re.findall(r"[\w']+", current)[1]
    identifier = f"{source}:{line_num}"

    BIBLIOGRAPHY[identifier] = FunctionReference(name, line_num, source)

    def add_ref(i, j):
        one_ref = " ".join(ref_raw[i:j]).replace("@", "_")
        kwargs = eval(one_ref)
        BIBLIOGRAPHY[identifier].short_purpose.append(kwargs["short_purpose"])
        BIBLIOGRAPHY[identifier].references.append(kwargs["reference"])
        return j

    reduce(add_ref, ref_lines)
