import inspect
import wrapt
from typing import NamedTuple, List


class FunctionReference(NamedTuple):
    name: str
    line: int
    source: str
    short_purpose: List[str] = []
    references: List[str] = []


class Biblio(dict):
    track_references: bool = False

    def __str__(self):
        index = 1
        output = ""
        for record in self.values():
            output += f"Referenced in: {record.name}"
            output += f"\nSource file: {record.source}"
            output += f"\nLine: {record.line}\n"
            for short, ref in zip(record.short_purpose, record.references):
                output += f"[{index}] {short} - {ref}"
                index += 1
            output += "\n"

        return output

    @property
    def references(self):
        """Return a list of unique references."""
        output = []
        for record in self.values():
            output = output + [ref for ref in record.references if ref not in output]

        return output


BIBLIOGRAPHY: Biblio = Biblio()


def tracking(enabled=True):
    """Enable the tracking of references."""
    global BIBLIOGRAPHY
    BIBLIOGRAPHY.track_references = enabled


def hexID(obj: str) -> str:
    return "{}".format(id(obj))


def insert_reference(*, short_purpose: str, reference: str):
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
        identifier = f"{wrapped.__name__} [{hexID(wrapped)}]"

        if (
            identifier in BIBLIOGRAPHY
            and reference in BIBLIOGRAPHY[identifier].references
        ):
            return wrapped(*args, **kwargs)

        if identifier not in BIBLIOGRAPHY:
            source = inspect.getsourcefile(wrapped)
            line = inspect.getsourcelines(wrapped)[1]
            BIBLIOGRAPHY[identifier] = FunctionReference(wrapped.__name__, line, source)

        BIBLIOGRAPHY[identifier].short_purpose.append(short_purpose)
        BIBLIOGRAPHY[identifier].references.append(reference)

        return wrapped(*args, **kwargs)

    return wrapper
