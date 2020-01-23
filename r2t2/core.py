import inspect
import wrapt
from typing import NamedTuple, List
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
            output = output + [ref for ref in record.references if ref not in output]

        return output

    def tracking(self, enabled=True):
        """Enable the tracking of references."""
        self.track_references = enabled


BIBLIOGRAPHY: Biblio = Biblio()


def add_reference(*, short_purpose: str, reference: str):
    """Decorator to link a reference to a function or method.

    Acts as a marker in code where particular alogrithms/data/... originates.
    General execution of code silently passes these markers, but remembers how and where
    they were called. Which markers were passed in a particular program run
    can be recalled with print_references().

    Arguments:
    short_purpose: Identify the thing being referenced (string)
    reference: The reference itself, in any sensible format.
    """

    @wrapt.decorator(enabled=lambda: BIBLIOGRAPHY.track_references)
    def wrapper(wrapped, instance, args, kwargs):
        source = inspect.getsourcefile(wrapped)
        line = inspect.getsourcelines(wrapped)[1]
        identifier = f"{source}:{line}"

        if (
            identifier in BIBLIOGRAPHY
            and reference in BIBLIOGRAPHY[identifier].references
        ):
            return wrapped(*args, **kwargs)

        if identifier not in BIBLIOGRAPHY:
            BIBLIOGRAPHY[identifier] = FunctionReference(wrapped.__name__, line, source)

        BIBLIOGRAPHY[identifier].short_purpose.append(short_purpose)
        BIBLIOGRAPHY[identifier].references.append(reference)

        return wrapped(*args, **kwargs)

    return wrapper
