Add Reference
=============

R2T2 works by decorating functions, classes or methods where particular
algorithms described in a paper are implemented
or data stored in a repository is used.
General execution of code silently passes these decorators,
but remembers how and where they were called.
The decorators include a short description of the thing being reference,
and the reference itself in any sensible format.

..  literalinclude:: ../examples/minimal.py
    :language: python

Several references can be added by stacking multiple ``@add_reference``
decorators. ::

..  literalinclude:: ../examples/mutiple.py
    :language: python
