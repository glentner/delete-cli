Configuration
=============


Environment Variables
---------------------

``TRASH_FOLDER``
^^^^^^^^^^^^^^^^

By default, the program will move objects to the ``~/.Trash`` folder. This is for consistency with
systems like *macOS* and most *Linux* distributions. In this way, the *empty trash* operation on
these systems will also remove anything put there by the ``delete`` program via the command line.

You can specify a different location via the ``TRASH_FOLDER`` environment variable. For example, in
your ``~/.bashrc`` or ``~/.bash_profile``:

.. code-block:: bash

    export TRASH_FOLDER=$HOME/.deleted


.. toctree::
    :maxdepth: 2
    :caption: Contents:
