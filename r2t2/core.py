import inspect
import wrapt
from typing import NamedTuple, List, Optional, Callable, Dict, Union
from functools import reduce
from pathlib import Path


class FunctionReference(NamedTuple):
    name: str
    line: int
    source: str
    short_purpose: List[str]
    references: List[str]


class Biblio(dict):
    track_references: bool = False

    def __init__(self):
        super().__init__()
        self._sources: Dict[str, Path] = {}

    def __str__(self):
        def add_record(out, record):
            index = 1
            out += f"Referenced in: {record.name}"
            out += f"\nSource file: {record.source}"
            out += f"\nLine: {record.line}\n"
            for short, ref in zip(record.short_purpose, record.references):
                out += f"\t[{index}] {short} - {ref}\n"
                index += 1
            out += "\n"
            return out

        return reduce(add_record, self.values(), "")

    @property
    def references(self):
        """Return a list of unique references."""
        output = []
        for record in self.values():
            output.extend(ref for ref in record.references if ref not in output)

        return output

    def tracking(self, enabled=True):
        """Enable the tracking of references."""
        self.track_references = enabled

    def add_source(self, source: Union[str, Path]) -> None:
        """Adds a bibliography source to the list of known sources.

        Args:
            source (str, Path): Path to the references source file. This must be a
                bibtex file.

        Raises:
            ValueError if the file is not bibtex.
            RuntimeError if the file does not exist.

        Returns:
            None
        """
        package = inspect.getmodule(inspect.stack()[1][0]).__name__.split(".")[0]
        src = Path(source)
        if src.suffix != ".bib":
            raise ValueError("References sources must be in bibtex format '.bib'")
        if not src.is_file():
            raise RuntimeError(f"References source file '{src}' does not exist!")
        self._sources[package] = src


BIBLIOGRAPHY: Biblio = Biblio()


def add_reference(
    *, short_purpose: str, reference: Optional[str] = None, doi: Optional[str] = None
) -> Callable:
    """Decorator to link a reference to a function or method.

    Acts as a marker in code where particular alogrithms/data/... originates.
    General execution of code silently passes these markers, but remembers how and where
    they were called. Which markers were passed in a particular program run
    can be recalled with `print(BIBLIOGRAPHY)`.

    One and only one method for providing the reference is allowed.

    Args:
        short_purpose (str): Identify the thing being referenced.
        reference (Optional, str): The reference itself, as a plain text string.
        doi (Optional, str): DOI of the reference.

    Returns:
        The decorated function.
    """
    if reference and doi:
        raise ValueError("Only one method for providing the reference is allowed.")
    elif reference:
        ref = reference
    elif doi:
        ref = doi if "doi.org" in doi else f"https://doi.org/{doi}"
    else:
        raise ValueError("No reference information provided!")

    @wrapt.decorator(enabled=lambda: BIBLIOGRAPHY.track_references)
    def wrapper(wrapped, instance, args, kwargs):
        source = inspect.getsourcefile(wrapped)
        line = inspect.getsourcelines(wrapped)[1]
        identifier = f"{source}:{line}"

        if identifier in BIBLIOGRAPHY and ref in BIBLIOGRAPHY[identifier].references:
            return wrapped(*args, **kwargs)

        if identifier not in BIBLIOGRAPHY:
            BIBLIOGRAPHY[identifier] = FunctionReference(wrapped.__name__, line, source,
                                                         [], [])

        BIBLIOGRAPHY[identifier].short_purpose.append(short_purpose)
        BIBLIOGRAPHY[identifier].references.append(ref)

        return wrapped(*args, **kwargs)

    return wrapper
