Diagnostic Expert Advisor
=========================

|workflow| |pyversion| |docs| |license| |black|

.. |pyversion| image:: https://img.shields.io/badge/python-v3.11.3-blue
.. |docs| image:: https://img.shields.io/readthedocs/diagnostic-expert-advisor
.. |license| image:: https://img.shields.io/github/license/jrc-combine/dea
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
.. |workflow| image:: https://github.com/JRC-COMBINE/DEA/actions/workflows/python-app.yml/badge.svg

The **D**\ iagnostric **E**\ xpert **A**\ dvisor is a lightweight toolkit to enable medical researchers to quickly get started with their work. 

.. image:: https://raw.githubusercontent.com/JRC-COMBINE/DEA/2cb2fa289e91d9aceae809ac30f624f8cb7968c1/img/cohort_overview.png
.. _flask: https://github.com/pallets/flask

This repository provides the tooling to rapidly launch into data exploration, model development and HPC processing. It is based on `Flask`_, one of the most popular Python web application frameworks and works with all your favorite data science tools. By default the DEA provides 

- Intuitive Dataset Structuring,
- Easy HPC Interfacing and
- Customizable Visualization

While the DEA offers suggestions, it does not enforce the use of any specific structures, layouts or libraries and researchers can decide themselves which tools best fit the job.

Installing
----------

Clone the repository and setup the environment:

.. code:: bash
   
   $ git clone git@github.com:JRC-COMBINE/DEA.git
   $ cd DEA
   $ conda create --name dea --file requirements.txt
   $ conda activate dea

Optionally download sample data:

.. code:: bash

   $ cd tests
   $ wget https://github.com/JRC-COMBINE/DEA/releases/download/v0.1.0-alpha/testdata.zip
   $ unzip testdata.zip  # data is located in DEA/tests/data, feel free to explore the structure!
   $ cd ..
   $ python quickstart.py # generate a cohort from the test data into DEA/dea/data

Finally start the Flask server:

.. code:: bash

   $ cd dea
   $ flask run  # add --debug to update on code change.


Where do I start?
-----------------

First of all you need to get your data into the DEA format. Luckily this is just a thin wrapper around Pandas DataFrames in the form of `encounters` and `cohorts`. You can think of `cohorts` as a list of `encounters`, with `encounters` being a single visit of a patient to the hospital. Such an `encounter` contains measurements over time (think heartrate) as well as static information (e.g. height) and some metadata. Once the data is in the correct format (or you adapted the DEA to your format), there is various ways to progress:

* Explore individual Encounters using  `PyGWalker <https://github.com/Kanaries/pygwalker>`_, through a "Tableau-style User Interface for visual analysis"
* Create custom visualizations and automate analysis for the whole cohort or individual encounters ( Go `here <https://diagnostic-expert-advisor.readthedocs.io/en/latest/usage/visualization.html>`_ )
* Run computationally expensive calculations in parallel on High-Performance Computing Infrastructure ( t.b.d )
* Use your usual workflow to develop ML models and deploy them to the DEA ( t.b.d. ) 
* Create customized filters to verify and test model behavior on specific groups of interest ( Go `here <https://diagnostic-expert-advisor.readthedocs.io/en/latest/usage/filters.html>`_ )

Contributing
------------

If you want to contribute to the DEA, please reference our `contribution guidelines`_

.. _contribution guidelines: https://diagnostic-expert-advisor.readthedocs.io/en/latest/contributing.html

Links
-----

-   Documentation: https://diagnostic-expert-advisor.readthedocs.io/en/latest/\
-   Source: https://github.com/JRC-COMBINE/DEA
-   Issue tracker: https://github.com/JRC-COMBINE/DEA/isssues
