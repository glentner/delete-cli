Manual Page for Delete
======================

Synopsis
--------

| delete *PATH* [*PATH* ...]


Description
-----------

The ``delete`` command accepts file paths and performs a simple move operation to a trash folder,
and possibly renames the file by adding a suffix.


Usage
-----

-h, --help          Show help message and exit.
-v, --version       Show the version number and exit.

Environment Variables
---------------------

``TRASH_FOLDER``

    By default, the program will move objects to the ``~/.Trash`` folder. This is for consistency
    with systems like macOS and most Linux distributions. In this way, the *empty trash* operation
    on these systems will also remove anything put there by the ``delete`` program via the command
    line. You can specify a different location via the ``TRASH_FOLDER`` environment variable. For
    example, in your ``~/.bashrc`` or ``~/.bash_profile``:

    .. code-block:: bash

        export TRASH_FOLDER=$HOME/.deleted


