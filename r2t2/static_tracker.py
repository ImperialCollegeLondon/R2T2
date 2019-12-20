from pathlib import Path
from collections import OrderedDict
import re
from typing import Union
import os


def locate_references(path: Union[Path, str]) -> OrderedDict:
    """Locates science_reference in path.

    It looks recursively for science_reference markers, taking note of the module, line
    short_purpose and actual reference string.

    Returns
        An Order dict where each key corresponds to a file name with references and each
        value is a list with the reference information as
        [line number, short_purpose, reference]
    """
    filenames = sorted(Path(path).rglob("*.py"))

    ref: OrderedDict = OrderedDict()
    sci_ref = re.compile(r"science_reference\(\"(.*?)\",\)")
    args = re.compile(r"\"(.*?)\"")

    for filename in filenames:
        ref[filename] = []
        code_str = []

        with open(filename, "r") as f:
            for num, line in enumerate(f):
                if "science_reference(" in line:
                    ref[filename].append([num + 1])

                code_str.append(line.strip())

            single = "".join(code_str).replace('""', "")

        results = sci_ref.findall(single)
        for i, ref_raw in enumerate(results):
            if '"' not in ref_raw:
                continue
            ref[filename][i].extend(args.findall('"' + ref_raw + '"'))

        ref[filename] = [p for p in ref[filename] if len(p) == 3]

    return ref


def to_markdown(references: OrderedDict, mdfile: Union[Path, str]) -> None:
    """Converts the references dictionary into a markdown file."""
    template = (
        "{id}. [{target}]({filename}) - Line={line}  \n"
        "\t**Short purpose:** {short}  \n"
        "\t**Reference:** {reference}  \n\n"
    )

    id = 1
    root = Path(mdfile).parent
    with open(mdfile, mode="w") as f:
        for path, refs in references.items():
            filename = os.path.relpath(path, root)
            for i, ref in enumerate(refs):
                f.write(
                    template.format(
                        id=id,
                        target=filename.replace("__", r"\_\_"),
                        filename=filename,
                        line=ref[0],
                        short=ref[1],
                        reference=ref[2],
                    )
                )
                id += 1
