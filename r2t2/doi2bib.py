"""The following code has been adapted from:

https://gist.github.com/jrsmith3/5513926
"""

import requests
from warnings import warn
from typing import Optional


def doi2bib(doi) -> Optional[str]:
    """Return a bibTeX string of metadata for a given DOI."""
    url = doi if "doi.org" in doi else f"https://doi.org/{doi}"
    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url, headers=headers)
    if "DOI Not Found" in r.text:
        warn(f"Reference with doi={doi} not found!", UserWarning)
        return None
    return r.text
