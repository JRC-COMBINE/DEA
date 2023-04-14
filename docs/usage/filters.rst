Filters
=======

Filters can be used to further specific cohorts. They are available in the encounter overview page. For example:

.. image:: https://raw.githubusercontent.com/JRC-COMBINE/DEA/main/img/filters.png

Above screenshot shows two filters: "Short Stay" and "Severe ARDS" active on the test data.  
With tags set up for the same criteria we can quickly verify the filters working correctly.

How to define filters?
----------------------
To add a filter append a name for it and a function to the FILTERS variable in :file:`dea/app.py`.
The filter function is called for every encounter and should return a boolean indicating whether to include the encounter or not.
If you want to run a study only on patients that are called "Boris" you could set up a Boris filter like this:

.. code:: python
    
    :lineos:
    :emphasize-lines: 5
    FILTERS = {
        "Short Stay": filter_short_stay,
        "Severe ARDS": filter_severe_ards,
        "Many Measurements": filter_many_measurements,
        "Boris": lambda encounter: encounter.patient.name == "Boris"  
    }

The filter will automatically create a new button in the filter section of the encounter overview page.
Customizing the visualization of the filters can be done by changing the template in :file:`dea/templates/encounter_list.html`.