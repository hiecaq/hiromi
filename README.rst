hiromi
======

Hiromi is a command line tool aiming at providing a convenient way to
update anime watching status, potentially for multiple recording
websites.

.. figure:: https://i.imgur.com/rNDSAEB.gif
   :alt: A demo showing the basic operation of hiromi

   demo

Usage
-----

::

    usage: hiromi [-h] [-V] {immigrate,list,update} ...

    Command line anime tracker.

    positional arguments:
      {immigrate,list,update}
        immigrate           Immigrate watched list from bangumi to MyAnimeList
        list                List local or remote watchlist
        update              Increment the target anime's watching status by 1

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         Show version and exit

See ``hiromi --help`` and ``hiromi COMMAND --help`` for details.

Requirements
------------

``hiromi`` only support ``python3``, and is only tested under
``python3.6.4``.

Installation
------------

This project is still under developing state.

.. code:: bash

    git clone https://github.com/quinoa42/hiromi.git
    cd hiromi
    pip install -e .
