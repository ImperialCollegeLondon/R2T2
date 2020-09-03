Output Format
=============

To have more control on the format of the output,
use the ``-f`` flag::

    $ python -m r2t2 run -f markdown some/subdirectory

And to have more control on where the output is written,
use the ``-o`` flag::

    $ python -m r2t2 static -o docs/list_of_references.md some/subdirectory

The contents of the output will be organised by decorated object in the order
they were encountered and contain the line where the decorator was found,
a link to that location,
and the list of the short purposes and the references itself.
For example::

    Referenced in: roasted_chicken  
    Source: [tests/test_r2t2.py](tests/test_r2t2.py:7)  
    Line: 7

        [1] Roasted chicken recipe - Great British Roasts, 2019
