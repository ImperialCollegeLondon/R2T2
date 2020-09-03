References
==========

R2T2 works by decorating functions, classes or methods
with ``@add_reference``
where particular algorithms described in a paper are implemented
or data stored in a repository is used.

In Function
-----------

..  literalinclude:: ../examples/minimal.py
    :language: python
    :lines: 1-11

In Class
--------

..  literalinclude:: ../examples/minimal_class.py
    :language: python
    :lines: 1-11

In Method
---------

..  literalinclude:: ../examples/minimal_method.py
    :language: python
    :lines: 1-12

Two or More References
----------------------

..  literalinclude:: ../examples/multiple.py
    :language: python
    :lines: 1-7

As Docstring
------------

R2T2 will parse the docstring searching for the DOI.

..  literalinclude:: ../examples/docstring_doi_reference.py
    :language: python
    :lines: 1-8

R2T2 will also search for Sphinx's ``cite`` directive.

..  literalinclude:: ../examples/docstring_sphinx_cite.py
    :language: python
    :lines: 1-5

