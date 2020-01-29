Configuration
=============

``delete`` has no real configuration other than where on the system to keep the trash
folder and its database, both of which are controlled by the below environment variables.


Environment Variables
---------------------

``TRASH_FOLDER``
^^^^^^^^^^^^^^^^

By default, the program will move objects to the ``~/.Trash`` folder. This is for
consistency with systems like macOS and most Linux distributions. In this way, the
*empty trash* operation on these systems will also remove anything put there by the
``delete`` program via the command line. You can specify a different location via the
``TRASH_FOLDER`` environment variable. For example, in your ``~/.bashrc``.

.. code-block:: bash

    export TRASH_FOLDER=$HOME/.deleted


``TRASH_DATABASE``
^^^^^^^^^^^^^^^^^^

By default, the path to the database is ``${TRASH_FOLDER}.db``, which would be
``~/.Trash.db`` if the ``TRASH_FOLDER`` environment variable is undefined. This path
*should not* be inside the trash folder. You can specify a different location via the
``TRASH_DATABASE`` environment variable. For example, in your ``~/.bashrc``.

.. code-block:: bash

    export TRASH_DATABASE=$HOME/.my_trash.db



.. toctree::
    :maxdepth: 2
    :caption: Contents:
