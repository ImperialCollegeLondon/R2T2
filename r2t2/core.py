import inspect
import wrapt
from typing import NamedTuple, List, Optional, Callable, Dict, Union
from functools import reduce, partial
from pathlib import Path
from warnings import warn

import bibtexparser as bp

from .doi2bib import doi2bib


class FunctionReference(NamedTuple):
    name: str
    line: int
    source: str
    package: str
    short_purpose: List[str]
    references: List[str]


class Biblio(dict):
    track_references: bool = False
    _processes: Dict[str, Callable] = {}

    @classmethod
    def register_process(cls, f: Optional[Callable] = None, name: Optional[str] = None):
        """Register a function for processing references in the registry.

        Args:
            f: Function to process references.
            name (str): Name of the type of reference to process, eg. plain, doi...

        Returns:
            The same input function
        """
        if f is None:
            return partial(cls.register_process, name=name)

        name = name if name else f.__name__

        cls._processes[name] = f
        return f

    def __init__(self):
        super().__init__()
        self._sources: Dict[str, Path] = {}
        self._sources_loaded: Dict[str, bp.bibdatabase.BibDatabase] = {}

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

    def clear(self) -> None:
        super().clear()
        self._sources.clear()
        self._sources_loaded.clear()

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
            RuntimeError if the package already has a reference.

        Returns:
            None
        """
        package = inspect.getmodule(inspect.stack()[1][0]).__name__.split(".")[0]
        src = Path(source)
        if src.suffix != ".bib":
            raise ValueError("References sources must be in bibtex format '.bib'")
        if not src.is_file():
            raise RuntimeError(f"References source file '{src}' does not exist!")
        if package in self._sources:
            raise RuntimeError(
                "A reference source for this package has already been added"
            )
        self._sources[package] = src

    def load_source(self, package: str) -> None:
        """Open the source for the given package."""
        with self._sources[package].open() as f:
            self._sources_loaded[package] = bp.load(f)

    def get_source(self, package: str) -> bp.bibdatabase.BibDatabase:
        """Provide the requested sources database."""
        if package not in self._sources_loaded:
            self.load_source(package)
        return self._sources_loaded[package]

    def add_entry_to_source(self, entry: dict, package: str) -> None:
        """Add entry to source and save it source for the given package."""
        self._sources_loaded[package].entries.append(entry)
        with self._sources[package].open() as f:
            bp.dump(self._sources_loaded[package], f)

    def process_ref(self, ref: FunctionReference) -> List[Dict]:
        """Process the reference keys and retrieves the full information."""
        self.get_source(ref.package)

        processed = []
        for refstr in ref.references:
            rtype, rstr = refstr.strip("[").split("]", 1)
            processed.append(self._processes[rtype](rstr, ref.package))

        return processed


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
        try:
            package = inspect.getmodule(inspect.stack()[1][0]).__name__.split(".")[0]
        except AttributeError:
            package = ""

        if identifier in BIBLIOGRAPHY and ref in BIBLIOGRAPHY[identifier].references:
            return wrapped(*args, **kwargs)

        if identifier not in BIBLIOGRAPHY:
            BIBLIOGRAPHY[identifier] = FunctionReference(
                wrapped.__name__, line, source, package, [], []
            )

        BIBLIOGRAPHY[identifier].short_purpose.append(short_purpose)
        BIBLIOGRAPHY[identifier].references.append(ref)

        return wrapped(*args, **kwargs)

    return wrapper


@Biblio.register_process("plain")
def process_plain(ref: str, *args, **kwargs) -> Dict:
    """ Process a plain string reference. Dummy function.

    Args:
        ref (str): The input reference string

    Returns:
        A dictionary with the reference string as "title", a unique ID equal to the hash
        of the reference string and an "ENTRYTYPE" equal to "misc".
    """
    return {"ID": hash(ref), "ENTRYTYPE": "misc", "title": ref}


@Biblio.register_process("bibtex")
def process_bibtex(ref: str, package: str, *args, **kwargs) -> Dict:
    """ Process a bibtex key reference.

    Args:
        ref (str): The bibtex key.
        package (str): The package from where to get the reference from.

    Raises:
        KeyError: If the reference source for that package does not contain the
            requested key.
    Returns:
        A dictionary with the reference full information
    """
    return BIBLIOGRAPHY.get_source(package).entries_dict[ref]


@Biblio.register_process("doi")
def process_doi(ref: str, package: str, *args, **kwargs) -> Dict:
    """ Process a doi key reference.

    First, it will look for the reference in the database for the given package. If it
    is not found there, it will retrieved it from the internet. If successful, the
    reference will be added to the database, so future requests to access this reference
    will be local.

    Args:
        ref (str): The doi of the reference.
        package (str): The package from where to get the reference from in the first
        instance and where to save the reference after getting it from the internet.

    Returns:
        A dictionary with the reference full information
    """
    db = BIBLIOGRAPHY.get_source(package)
    for entry in db.entries:
        out = entry if entry.get("doi") == ref else None
        if out:
            return out

    out = doi2bib(ref)
    if out:
        BIBLIOGRAPHY.add_entry_to_source(bp.loads(out), package)
        return db.entries[-1]

    warn(
        f"Reference with doi={ref} not found!", UserWarning,
    )
    return {}
