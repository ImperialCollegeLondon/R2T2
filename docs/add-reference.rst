Add Reference
=============

R2T2 works by decorating functions, classes or methods where particular
algorithms described in a paper are implemented
or data stored in a repository is used.
General execution of code silently passes these decorators,
but remembers how and where they were called.
The decorators include a short description of the thing being reference,
and the reference itself in any sensible format. ::

    from r2t2 import add_reference
    ...
    @add_reference(short_purpose="Original implementation of R2T2", 
                      reference="Diego Alonso-Álvarez, et al."
                                "(2018, February 27). Solcore (Version 5.1.0). Zenodo."
                                "http://doi.org/10.5281/zenodo.1185316")
    def my_great_function():
        pass

Several references can be added by stacking multiple ``@add_reference``
decorators. ::

    @add_reference(short_purpose="some comment",  reference="Reference 1")
    @add_reference(short_purpose="another comment",  reference="Reference 2")
    def my_great_function():
        pass
