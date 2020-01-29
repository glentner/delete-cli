Manual Page for Delete
======================

Synopsis
--------

| delete *PATH* [*PATH* ...]
| delete --restore *PATH* [*PATH* ...]
| delete --empty
| delete --list


Description
-----------

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


Usage
-----

--list           
    List objects and their original path.

--empty          
    Empty the trash.

--restore       
    Restore one or more items.

-h, --help           
    Show help message and exit.

-v, --version        
    Show the version number and exit.


Environment Variables
---------------------

``TRASH_FOLDER``

    By default, the program will move objects to the ``~/.Trash`` folder. This is for
    consistency with systems like macOS and most Linux distributions. In this way, the
    *empty trash* operation on these systems will also remove anything put there by the
    ``delete`` program via the command line. You can specify a different location via
    the ``TRASH_FOLDER`` environment variable. For example, in your ``~/.bashrc``.

    .. code-block:: bash

        export TRASH_FOLDER=$HOME/.deleted

``TRASH_DATABASE``

    By default, the path to the database is ``${TRASH_FOLDER}.db``, which would be
    ``~/.Trash.db`` if the ``TRASH_FOLDER`` environment variable is undefined. This path
    *should not* be inside the trash folder. You can specify a different location via
    the ``TRASH_DATABASE`` environment variable. For example, in your ``~/.bashrc``.

    .. code-block:: bash

        export TRASH_DATABASE=$HOME/.my_trash.db


Examples
--------

Deleting files and folders is as simple as:

.. code-block:: bash

    delete file1.txt file2.txt folderA

Files or folders that get deleted with the same basename will have a suffix added before
the extension (e.g., ``file1.1.txt``, ``file1.2.txt``, ...).

Restore files using their basename (in the trash), their full path (in the trash) or
their original full path.

.. code-block:: bash

    delete --restore file1.txt
    delete --restore $TRASH_FOLDER/file2.txt
    delete --restore /original/path/folderA

List the contents of the trash along with their original full paths.

.. code-block:: bash

    delete --list

Use ``--empty`` to completely empty the trash. This does not remove the
``$TRASH_FOLDER``. It iterates through the full listing of contents from the
``$TRASH_DATABASE``. If anything is left in the directory an error is logged.

.. code-block:: bash

    delete --empty


Recommendations
---------------

Add the following to your shell's login profile to shorten the invocation.

.. code-block:: bash

    alias del="delete"


See Also
--------

rm(1), sqlite3(1)


Bugs
----

* On *macOS* systems the default ``~/.Trash`` is protected and does not allow a listing
  of the directory. ``delete`` functions normally aside from an error message being printed
  when using ``--empty``.
