Runtime tracker
===============

Which markers were passed when running a particular script ``my_script.py`` can be
recalled with::

    $ python -m r2t2 run my_script.py

This prints a list of markers passed in the script run and recursively in any
dependency used by the program.
Input arguments needed by the script can be added after its name. ::

    $ python -m r2t2 run my_script.py -- arg1 arg2
