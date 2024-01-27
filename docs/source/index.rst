Delete
======

*A simple, cross-platform, command line move-to-trash.*

.. image:: https://img.shields.io/badge/license-Apache-blue.svg?style=flat
    :target: https://www.apache.org/licenses/LICENSE-2.0
    :alt: License

.. image:: https://img.shields.io/pypi/v/delete-cli.svg
    :target: https://pypi.org/project/delete-cli
    :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/delete-cli.svg?logo=python&logoColor=white&style=flat
    :target: https://pypi.org/project/delete-cli
    :alt: Python Versions

.. image:: https://readthedocs.org/projects/delete-cli/badge/?version=latest&style=flat
    :target: https://delete-cli.readthedocs.io
    :alt: Documentation

.. image:: https://pepy.tech/badge/delete-cli
    :target: https://pepy.tech/badge/delete-cli
    :alt: Downloads

Release v\ |release|. (:ref:`Installation <install>`)

-------------------

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

-------------------

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    getting_started
    configuration
