delete - a command line move-to-trash
=====================================

The ``delete`` command is a simple alternative to using the standard ``rm`` command.
Using ``rm`` as a matter of course can be dangerous and prone to mistakes. Once a file is
unlinked with ``rm`` it cannot be recovered (without having backups).

All major graphical environments offer a "move to trash" option. This does a clean move
operation to a "trash" folder. Once a file as been put in the trash it can be recovered
easily. Periodically, the trash can be emptied if desired.

``delete`` is a command line implementation of this metaphor. It maintains a basic
``sqlite3`` database of files and folders put in the trash. Using the ``--list`` option
will list the contents. Using ``--restore`` will restore a file or folder from the trash.
Using ``--empty`` will purge anything put in the trash by ``delete``.


.. toctree::
    :maxdepth: 2
    :caption: Contents:

    getting_started
    configuration
