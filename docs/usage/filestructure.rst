File Structure
==============

Reading and writing data can be a complex task. For brevity and simplicity we support two different approaches by default. The majority of user-facing data loading will happen through csv files, with HPC data sharing happening through joblib. This comes with the advantage of being simple and widely understood, as well as human readable. While more efficient and elegant solutions, thus as `arrow`_ files or timeseries focussed databases, such as `influxdb`_, are very viable alternatives, we do not support them by default.

.. _arrow: https://arrow.apache.org/
.. _influxdb: https://www.influxdata.com/

CSV Data Structure
------------------

The csv data structure is a simple and widely understood format. It is also very easy to read and write. The main disadvantage is that it is not very efficient, and thus not suitable for very large datasets.

.. code-block:: bash
    
    Data
    ├── Cohort A
    |   ├── Encounter 1
    |   |   ├── File dynamic.csv
    |   |   ├── File processed.csv
    |   |   ├── File intermediate_results.csv
    |   |   └── File predictions.csv
    │   ├── Encounter 2
    |   |   ├── File ...
    │   ├── Encounter ...
    |   |   └── ...
    │   ├── static.csv
    │   ├── comorbidities.csv
    │   └── analysis.csv
    ├── Cohort B
    │      └── ...

Basically Data is grouped by Cohort/Encounter and have inidividual files for each. 
Rule of thumb: if the data is static, we handle it on a cohort level, if it is dynamic we handle it on an encounter level.

While it would be possible to have static data stored at an encounter level, and we do so in the in-memory data structure - we do not want to create too many individual files, so for now we will accept the small increase in complexity.

HPC Data Sharing
----------------

To distribute data to HPC clusters we use joblib. This is a very efficient and elegant solution, but it is not human readable. We therefore use it for data sharing, but not for data storage. Keep in mind that data stored in this format should be recreatable at every time, as changes in the code might invalidate the data.

Custom Data format
------------------

Extending the DEA to store in custom data formats can be done at various levels of complexity. Utilizing a different folder structure only requires a rewrite of the default loading logic in :meth:`dea.cohort.Cohort.from_path` and :meth:`dea.cohort.Cohort.save`. If you want to change the data format to e.g. arrow_ or use `joblib`_ everywhere (**not recommended!**), adjust the :meth:`dea.encounter.Encounter.from_path` and :meth:`dea.encounter.Encounter.save` methods.

.. _joblib: https://joblib.readthedocs.io/en/latest/

Future Concept
--------------

If the need for more modularity exists here, we will consider a more sophisticated approach, such as a plugin system. However, for now we will keep it simple.

