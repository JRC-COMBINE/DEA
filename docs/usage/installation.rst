Installation
============

This project is meant to be forked and modified, so it is not available on PyPI. To install it, clone the repository and install the requirements.

.. code:: bash
   
   $ git clone git@github.com:JRC-COMBINE/DEA.git
   $ cd DEA
   $ conda create --name dea --file requirements.txt
   $ conda activate dea

The DEA is run by flask. To start the server, run the following command from the root directory of the project. Line 3 shows an alternative call that can be used to run the server in debug mode. Be careful, it also exposes the server to the outside world by changing the host to 0.0.0.0. This is convenient for remote debugging, but it is not recommended for production.

.. code-block:: bash
    :linenos:

    $ cd dea/
    $ flask run
    $ #flask --debug run --host 0.0.0.0 -- port 5005