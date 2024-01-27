Delete
======

*A simple, cross-platform, command-line move-to-trash.*

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License

.. image:: https://img.shields.io/pypi/v/delete-cli.svg
    :target: https://pypi.org/project/delete-cli
    :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/delete-cli.svg?logoColor=white
    :target: https://pypi.org/project/delete-cli
    :alt: Python Versions

.. image:: https://readthedocs.org/projects/delete-cli/badge/?version=latest&color=green
    :target: https://delete-cli.readthedocs.io
    :alt: Documentation

.. image:: https://pepy.tech/badge/delete-cli
    :target: https://pepy.tech/badge/delete-cli
    :alt: Downloads


But why?
--------

The ``del`` command is a simple alternative to using the standard ``rm`` command.
Using ``rm`` as a matter of course can be dangerous and prone to mistakes. Once a file is
unlinked with ``rm`` it cannot be recovered (without having backups).

All major graphical environments offer a "move to trash" option. This does a clean move
operation to a "trash" folder. Once a file as been put in the trash it can be recovered
easily. Periodically, the trash can be emptied if desired.

``del`` is a command-line implementation of this metaphor. It maintains a basic
``sqlite3`` database of files and folders put in the trash. Using the ``--list`` option
will list the contents. Using ``--restore`` will restore a file or folder from the trash.
Using ``--empty`` will purge anything put in the trash by ``del``.


Installation
------------

If you already have Python 3.12+ on your system, you can install ``del`` using Pip.

.. code-block:: bash

    pip install delete-cli


Basic Usage
-----------

Calling ``del`` with no arguments or with the ``--help`` flag yield typically Unix
style behavior, print a usage or help statement, respectively. For detailed usage and
examples you can read the manual page, ``man del``.

Deleting files and folders is as simple as:

.. code-block:: bash

    del file1.txt file2.txt folderA

Files or folders that get deleted with the same basename will have a suffix added before
the extension (e.g., ``file1.1.txt``, ``file1.2.txt``, ...).

Restore files using their basename (in the trash), their full path (in the trash) or
their original full path.


Documentation
-------------

Documentation is available at `delete-cli.readthedocs.io <https://delete-cli.readthedocs.io>`_.
For basic usage information on the command-line use: ``del --help``. For a more comprehensive
usage guide on the command line you can view the manual page with ``man del``.


Contributions
-------------

Contributions are welcome in the form of suggestions for additional features, pull requests with
new features or bug fixes, etc. If you find bugs or have questions, open an *Issue* here. If and
when the project grows, a code of conduct will be provided along side a more comprehensive set of
guidelines for contributing; until then, just be nice.
