Getting Started
===============

.. _install:

Installation
------------

If you already have Python 3.12 on your system, you can install ``del`` using Pip.

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

.. code-block:: bash

    del --restore file1.txt
    del --restore $TRASH_FOLDER/file2.txt
    del --restore /original/path/folderA

List the contents of the trash along with their original full paths.

.. code-block:: bash

    del --list

Use ``--empty`` to completely empty the trash. This does not remove the
``$TRASH_FOLDER``. It iterates through the full listing of contents from the
``$TRASH_DATABASE``. If anything is left in the directory an error is logged.

.. code-block:: bash

    del --empty


Known Issues
------------

* On *macOS* systems the default ``~/.Trash`` is protected and does not allow a listing
  of the directory. ``del`` functions normally aside from an error message being printed
  when using ``--empty``.


.. toctree::
    :maxdepth: 2
    :caption: Contents:
