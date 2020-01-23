import os
from pathlib import Path
from typing import Union, Callable, Optional

from r2t2 import BIBLIOGRAPHY


REGISTERED_WRITERS = dict()
"""Available writers to produce the output."""


def register_writer(fun: Optional[Callable] = None, name: Optional[str] = None):
    """Registers a writer in the writers registry."""
    if fun is None:
        return lambda x: register_writer(x, name=name)
    name = name if name else fun.__name__
    REGISTERED_WRITERS[name] = fun
    return fun


@register_writer(name="markdown")
def markdown(mdfile: Union[Path, str]) -> None:
    """Converts the references dictionary into a markdown file."""
    template_name = (
        "Referenced in: {name}  \n"
        "Source: [{source}]({source}:{line})  \n"
        "Line: {line}\n\n"
    )
    template_ref = "\t[{index}] {short} - {ref}  \n"

    if not str(mdfile).endswith(".md"):
        mdfile = str(mdfile) + ".md"

    root = Path(mdfile).parent
    with open(mdfile, mode="w") as f:
        for record in BIBLIOGRAPHY.values():
            source = os.path.relpath(record.source, root)
            f.write(
                template_name.format(name=record.name, source=source, line=record.line)
            )
            for i, (short, ref) in enumerate(
                zip(record.short_purpose, record.references)
            ):
                f.write(template_ref.format(index=i + 1, short=short, ref=ref))


@register_writer(name="terminal")
def terminal(mdfile: Union[Path, str]) -> None:
    """The output is just the Bibliography printed into the terminal."""
    print(BIBLIOGRAPHY)
