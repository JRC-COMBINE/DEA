Model Development
=================

The DEA itself does not imposed any boundaries on techniques and environments used to develop models. By wrapping :class:`pandas.DataFrame` closely most of the common Python data science libraries can be used. To use the :meth:`dea.Cohort` and :meth:`dea.Encounter` wrappers to develop a model e.g. in PyTorch or TensorFlow you can use the :meth:`dea.Encounter.dynamic` member to access the DataFrame directly. The :meth:`dea.Cohort.to_pandas` method provides a convenient way to convert the cohort to a stacked :class:`pandas.DataFrame`.