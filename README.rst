Diagnostic Expert Advisor
=========================

|workflow| |pyversion| |docs| |license| |black|

.. |pyversion| image:: https://img.shields.io/badge/python-v3.10.9-blue
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

Clone the repository, setup the environment and start hacking away:

.. code:: bash
   
   $ git clone git@github.com:JRC-COMBINE/DEA.git
   $ cd DEA
   $ conda create --name dea --file requirements.txt
   $ conda activate dea
   $ cd dea/
   $ flask run
   $ #flask --debug run --host 0.0.0.0 -- port 5005


Where do I start?
-----------------

First you want to create DataLoaders from your data sources. An example script can be found in `dea/data_generation_example.py` and adapted accordingly. The cohorts created this way are the basis for all further analysis. You can always change the cohort you are working on in the DEA. Examples for customization include:

* Cohort-level analysis can be integrated into `overview.html` and the `overview` function in `dea/app.py` respectively
* Per-Patient level analysis can be integrated into `encounter.html` and the `encounter` function in `dea/app.py` respectively
* Filters can be added to `encounter_list` in `dea/app.py`

Contributing
------------

If you want to contribute to the DEA, please fork the repository and create a pull request.

Links
-----

-   Documentation: https://diagnostic-expert-advisor.readthedocs.io/en/latest/\
-   Source: https://github.com/JRC-COMBINE/DEA
-   Issue tracker: https://github.com/JRC-COMBINE/DEA/isssues
