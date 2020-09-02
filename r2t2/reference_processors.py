from typing import Callable, Dict
from functools import partial, lru_cache
from abc import ABC, abstractmethod
import re


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
    match = re.findall(r'([\w.-/\\:\s]+)', ref)
    if len(match) != 2:
        raise ValueError(f"Could not process reference {ref}")

    return getattr(PROCESSORS[match[0]](match[1]), output_format)


class ProcessorBase(ABC):
    """Base class for all reference processors."""

    def __init__(self, ref):
        self._ref = ref

    @abstractmethod
    def plain(self) -> str:
        """Return the reference as plain text in a sensible format."""

    @abstractmethod
    def bibtex(self) -> str:
        """Return the reference as a bibtex entry."""
