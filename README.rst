Diagnostic Expert Advisor
=========================

|pyversion| |docs| |license|

.. |pyversion| image:: https://img.shields.io/badge/python-v3.10.9-blue?style=for-the-badge&logo=python
.. |docs| image:: https://img.shields.io/readthedocs/diagnostic-expert-advisor?style=for-the-badge
.. |license| image:: https://img.shields.io/github/license/jrc-combine/dea?style=for-the-badge

The **D**\ iagnostric **E**\ xpert **A**\ dvisor is a lightweight toolkit to enable medical researches to quickly get started with their work. 
It is based on `Flask`_ and written purely in Python.  

.. image:: https://raw.githubusercontent.com/JRC-COMBINE/DEA/2cb2fa289e91d9aceae809ac30f624f8cb7968c1/img/cohort_overview.png
.. _flask: https://github.com/pallets/flask

Installing
----------

Clone the repository, setup the environment and start hacking away:
.. code-block:: text
    $ git clone git@github.com:JRC-COMBINE/DEA.git  
    $ cd DEA  
    $ conda create --name dea --file requirements.txt  
    $ conda activate dea  
    $ flask run  
..

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
