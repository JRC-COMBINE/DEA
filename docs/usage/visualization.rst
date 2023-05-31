Visualization
=============

Visualizations in the DEA can be build through any module that results in html-embeddable plots.  

This could just be generated matplotlib file::`myplot.png` files, or it could be fancy interactive visualizations. The default implementation uses`bokeh`_ for beautiful and customizable plots like this:

.. image:: https://user-images.githubusercontent.com/1078448/190840954-dc243c99-9295-44de-88e9-fafd0f4f7f8a.jpg
.. _bokeh: https://bokeh.org/

(Image borrowed from the bokeh project site)

Adding Visualizations
---------------------

There are two places where visualizations can be added to the DEA, to add visualizations on cohort level, reference the :meth:`dea.app.overview` route, which passes the plot created in :meth:`dea.app.plot_cohort_hist`. 

.. image:: https://raw.githubusercontent.com/JRC-COMBINE/DEA/main/img/cohort_view.png

To add visualizations on the encounter level, reference the :meth:`dea.app.route_encounter` route, which creates the plot inline and also shows the `pygwalker`_ integration.

.. image:: https://raw.githubusercontent.com/JRC-COMBINE/DEA/main/img/encounter_view.png
.. _pygwalker: https://github.com/Kanaries/pygwalker

Bokeh Visualization example
---------------------------

.. code-block:: python

    X = df.index
    features = df.columns
    p = figure(
        title="Example Plot",
        sizing_mode="scale_width",
    )
    for y in features:
        p.line(
            X,
            e.loc[y],
            line_width=2,
            legend_label=y,
            color=Category20[len(features)][features.index(y)],
        )
    p_html_str = file_html(p, CDN)
    plots = [p_html_str]  # plots is a list of plots that will be displayed in the DEA
