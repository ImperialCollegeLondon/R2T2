Installation
============

First, download the source code::

    $ git clone git@github.com:ImperialCollegeLondon/R2T2.git

Second, install it and all development dependencies.
We use Poetry_ to automate and simplify development tasks
and you can set up your development environment like this::

    $ cd R2T2
    $ python -m pip install poetry # if you haven't already installed it
    $ poetry install

Poetry will set up a virtualenv for you to isolate the dependencies.
You can run commands in this virtualenv using ``poetry run <cmd>``;
for example, you can run the test suite like this::

    $ poetry run pytest

If you prefer, you can start a shell session in the virtualenv
and run commands like this::

    $ poetry shell
    Spawning shell within /home/jez/.cache/pypoetry/virtualenvs/r2t2-zSZaY5UC-py3.8

    $ pytest

Useful tools
============

The following development tools are automatically installed by ``poetry install``:

pytest_
    To find and run tests.
    Also includes the flake8, mypy and coverage plugins
    which will check code style, datatypes and test coverage respectively.

bump2version_
    Used to increment version numbers in all the right places
    when making a new release.

.. _Poetry: https://python-poetry.org/
.. _pytest: https://docs.pytest.org/en/stable/
.. _bump2version: https://github.com/c4urself/bump2version/
