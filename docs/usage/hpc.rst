High Performance Computing
==========================

The DEA allows for easy integration with high performance computing (HPC) clusters. By default the SLURM controller used at many universities is supported. The best part? You don't have to change anything in your code! The DEA will automatically submit your jobs to the HPC cluster if you configure it correctly. If no HPC account is setup up, the DEA will run the jobs locally, but still in parallel.

How to setup your HPC account
-----------------------------
The account is defined in :file:`dea/app.py`, using the :file:`dea/slurmbinder.py` module. The default configuration contains the following:

- paths for logging (output and error logs)
- time limit
- memory limit
- number of cores
- account name

Any parameter that can be passed to SLURM can be set here. Applicable parameters are listed in the `SLURM documentation <https://slurm.schedmd.com/sbatch.html>`_.

Which methods are parallelised?
-------------------------------

By default the :meth:`dea.Cohort.process` method is run on the HPC, while many other methods, such as loading and saving data, are run locally. Additional methods can be run on the HPC by passing the method to be moved to HPC to :meth:`dea.Cohort.hpc_bridge.arrayjob`. Check the :meth:`dea.Cohort.hpc_bridge.arrayjob` documentation for more information.