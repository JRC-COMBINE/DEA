Quickstart
==========

To get started clone the DEA repository and setup a conda environment for its dependencies

.. code:: bash
   
   $ git clone git@github.com:JRC-COMBINE/DEA.git
   $ cd DEA
   $ conda create --name dea --file requirements.txt

You can use various sources for your data, for example from the `MIMIC-III dataset <https://physionet.org/content/mimiciii/1.4/>`_.
For simplicities sake we provide testdata_ which can be used to get started quickly. 
Place the data in :file:`dea/tests/data` and continue following this guide.

.. _testdata: https://github.com/JRC-COMBINE/DEA/releases/download/v0.1.0-alpha/testdata.zip

First of all we need to convert the original data format into DEA encounters. The cohort class conveniently can be used for that.
For our testdata they are already organized as cohort/encounter/data.csv, so we can just pass the root folder to the cohorts load method.

.. code-block:: python

    from dea.cohort import Cohort
    coh = Cohort.from_path("../tests/data")
    coh.save("data/test")

Alternatively you can create your Encounters manually and add them to the cohort.

.. code-block:: python

    from dea.cohort import Cohort
    coh = Cohort()
    for my_data in my_data_source:
        e = Encounter(my_data.id, extract_dynamic_data(my_data), static_data_mapping[my_data.id])
        coh.encounters.append(e)
    coh.static = exotic_custom_format_to_df(static_data_mapping)
    coh.save("data/test")

With the data prepared we can now launch the DEA and start interacting with our cohort.

.. code-block:: bash

    $ conda activate dea
    $ cd dea/
    $ flask run --debug  # this ensures changes to the code are reflected immediately

Now we can open the DEA in our browser at http://localhost:5000/ and start exploring our cohort.
