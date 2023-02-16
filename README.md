![](https://img.shields.io/badge/python-v3.10.9-blue?style=for-the-badge&logo=python) ![Read the Docs](https://img.shields.io/readthedocs/diagnostic-expert-advisor?style=for-the-badge) ![GitHub](https://img.shields.io/github/license/jrc-combine/dea?style=for-the-badge)
# Diagnostic Expert Advisor
The **D**iagnostric **E**xpert **A**dvisor is a lightweight toolkit to enable medical researches to quickly get started with their work.  
It is based on [Flask](https://github.com/pallets/flask) and written purely in Python.  

![](https://raw.githubusercontent.com/JRC-COMBINE/DEA/2cb2fa289e91d9aceae809ac30f624f8cb7968c1/img/cohort_overview.png)

### Input Data Format

Use the dea_tools utility package to generate a cohort. A `DataLoader` is expected as input.

### How to run DEA

The DEA is designed to be run on the cluster so it can easily deploy SLURM jobs.  
Therefore usually one would want to run the interface on a SLURM job.  

An exemplatory startup script is available (`dea.job`) or you can start an interactive job and run the DEA manually.  

`srun --job-name "Diagnostic Expert Advisor" --cpus-per-task 32 --mem 120G --time 8:00:00 --pty zsh`

By default the port used is `5000`. The port needs to be tunneled through the cluster architecture to be accessible:  

`ssh -N -L 5000:final-hpc-node:5000 my-username@login-node.my-hpc.de`

### Setting up the Environment

Use conda to create a virtual environment with all requirements.  
Development was testen on Python 3.10, but all versions should work.  

`conda create --name dea --file requirements.tx`

Requirements are listed in `requirements.txt`, most notably:  

- tqdm
- flask
- numpy
- pandas
- pandas_bokeh
- openpyxl

### Running the App

`flask run --host 0.0.0.0`
