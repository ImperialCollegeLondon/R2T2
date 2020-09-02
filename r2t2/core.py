import inspect
import wrapt
from typing import NamedTuple, List, Optional, Callable
from functools import reduce


class FunctionReference(NamedTuple):
    name: str
    line: int
    source: str
    short_purpose: List[str] = []
    references: List[str] = []


class Biblio(dict):
    track_references: bool = False

    def __str__(self):
        def add_record(out, record):
            index = 1
            out += f"Referenced in: {record.name}"
            out += f"\nSource file: {record.source}"
            out += f"\nLine: {record.line}\n"
            for short, ref in zip(record.short_purpose, record.references):
                out += f"\t[{index}] {short} - {ref.split(']', 1)[-1]}\n"
                index += 1
            out += "\n"
            return out

        return reduce(add_record, self.values(), "")

    @property
    def references(self):
        """Return a list of unique references."""
        output = []
        for record in self.values():
            output = output + [ref for ref in record.references if ref not in output]

        return output

    def tracking(self, enabled=True):
        """Enable the tracking of references."""
        self.track_references = enabled


BIBLIOGRAPHY: Biblio = Biblio()


def add_reference(
    *,
    short_purpose: str,
    reference: Optional[str] = None,
    doi: Optional[str] = None,
    bibtex_key: Optional[str] = None,
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
        bibtex_key (Optional, str): key of the reference in bibtex file.

    Returns:
        The decorated function.
    """
    if (reference and doi) or (reference and bibtex_key) or (doi and bibtex_key):
        # TODO make this conditional more flexible
        raise ValueError("Only one method for providing the reference is allowed.")
    elif reference:
        ref = f"[plain]{reference}"
    elif doi:
        ref = f"[doi]{doi}" if "doi.org" in doi else f"[doi]https://doi.org/{doi}"
    elif bibtex_key:
        ref = f"[bibtex]{bibtex_key}"
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
            BIBLIOGRAPHY[identifier] = FunctionReference(wrapped.__name__, line, source)

        BIBLIOGRAPHY[identifier].short_purpose.append(short_purpose)
        BIBLIOGRAPHY[identifier].references.append(ref)

        return wrapped(*args, **kwargs)

    return wrapper
