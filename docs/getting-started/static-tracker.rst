Static tracker
==============

R2T2 can be used to provide a list of all references that a
given package is based on
(i.e. **all** the ``add_reference`` decorators it contains)
and not just those crossed by a particular run of a script using the package.

For using this method,
simply run in the terminal::

    $ python -m r2t2

which will scan all the Python files recursively
starting in the current directory.
By default,
it prints the results in the terminal.
To analyse a single file,
use the flag ``-s`` (from *static*)
to prevent r2t2 to treat it as a script to run::

    $ python -m r2t2 -s my_script.py

To extract dois from the docstrings of a script, pass the ``--docstring`` flag::

    $ python -m r2t2 --docstring -s my_script.py

Similarly, to extract dois from the markdown cells of a Jupyter notebook::

    $ python -m r2t2 --notebook -s my_notebook.ipynb
