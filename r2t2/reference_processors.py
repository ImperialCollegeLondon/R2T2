from typing import Callable, Dict
from functools import partial, lru_cache
from abc import ABC, abstractmethod
import re
import bibtexparser

from r2t2 import BIBLIOGRAPHY


PROCESSORS: Dict[str, Callable] = {}
"""Dictionary of available processors."""


def register_processor(f: Callable = None, name: str = None) -> Callable:
    """Register a reference processor.

    Args:
        f (callable): Function processing the reference string.
        name (str): Name of the processor.

    Returns:
        The input processor.
    """
    if f is None:
        return partial(register_processor, name=name)

    name = name if name else f.__name__
    PROCESSORS[name] = f

    return f


@lru_cache
def process_reference(ref: str, output_format: str = "plain"):
    """Process the reference string in the chosen format.

    This function is cached, so multiple calls with identical arguments are processed
    faster, specially useful when information needs to be read from a file or retrieved
    from the internet.

    Args:
        ref (str): The reference string. Should start with [XXX], where XXX is one of
            the known processors.
        output_format (str): The format the reference should be provided
            ("plain" or "bibtex").

    Returns:
        The reference in the requested format.
    """
    match = re.findall(r"([\w.-/\\:\s]+)", ref)
    if len(match) != 2:
        raise ValueError(f"Could not process reference {ref}")

    return getattr(PROCESSORS[match[0]](match[1]), output_format)


class ProcessorBase(ABC):
    """Base class for all reference processors."""

    def __init__(self, source=None):
        self.source = source

    @abstractmethod
    def plain(self) -> str:
        """Return the reference as plain text in a sensible format."""

    @abstractmethod
    def bibtex(self) -> str:
        """Return the reference as a bibtex entry."""


@register_processor(name="bibtex")
def BibtexProcessor(source=None):
    """Parses BIBLIOGRAPHY records based on key/ID of a bibtex database."""

    # Parse the bibtex source file into a dict
    # The key is the bibtex key
    with open(source) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    # Create a list of IDs for quick look-up
    ids = [entry["ID"] for entry in bib_database.entries]

    # Go through the records in BIBLIOGRAPHY and parse .references
    # We assume .references should be an ID in bib_database
    # If not, we print a warning but leave it as is
    for record in BIBLIOGRAPHY.values():
        for idx, reference in enumerate(record.references):
            if str.startswith(reference, "[bibtex]"):
                reference = reference[
                    8:
                ]  # this should be dealt with elsewhere but here's a catch
            if reference in ids:
                # the following is really not ideal
                # but bibtexparse doesn't seem to offer a function
                # to go from an entry to a string
                index = ids.index(reference)
                entry_dict = bib_database.entries[index]
                entry_string = "{0} by {1} ({2})".format(
                    entry_dict["title"], entry_dict["author"], entry_dict["year"]
                )  # TODO how to catch if a field is missing?
                record.references[idx] = entry_string
            else:
                print(
                    f"{reference} not found in the bibtex database."
                )  # TODO how to better log this?
