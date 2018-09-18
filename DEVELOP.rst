Using the development buildout
------------------------------

Create a virtualenv in the package::

    $ pyenv virtualenv msgraph
    $ pyenv local msgraph

Install package as editable with pip::

    $ ./bin/pip install -e .

Run pytest::

    $ pytest
