Quickstart
==========

To get started clone the DEA repository and setup a conda environment for its dependencies

.. code:: bash
   
   $ git clone git@github.com:JRC-COMBINE/DEA.git
   $ cd DEA
   $ conda create --name dea --file requirements.txt

You can use various sources for your data, for example from the `MIMIC-III dataset <https://physionet.org/content/mimiciii/1.4/>`_.
As the setup can be quite complicated and some prerequisits need to be met, we use simulated testdata for the quickstart.
You can find the data in the `tests/data` folder.

First of all we need to convert the csv files into our encounter format. The cohort class conveniently can be used for that.
For simplicity we save the cohort as a joblib file. This is a compressed pickle file and can be loaded with the ``load`` function.
If interfacing with other tools is needed, the cohort can also be saved as collection of csv files per encounter instead by providing a directory to the save method.

.. code-block:: python

    coh = Cohort("tests/data")
    coh.save("data/testcohort.joblib")

With the data prepared we can now launch the DEA and start interacting with our cohort.

.. code-block:: bash

    $ conda activate dea
    $ cd dea/
    $ flask run --debug  # this ensures changes to the code are reflected immediately

Now we can open the DEA in our browser at http://localhost:5000/ and start exploring our cohort.