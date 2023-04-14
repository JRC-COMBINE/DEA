from __future__ import annotations
import subprocess
from string import Template
from dea.encounter import Encounter
from pathlib import Path
from typing import List

import logging

class SlurmBinder():
    """This class holds information to pass onto every Slurm jobscript and provides methods for creating them."""
    def __init__(self, slurm_output, slurm_error, slurm_time, slurm_mem, slurm_account):
        """"
        Parameters
        ----------
        slurm_output : str
            Path to the directory where the log files should be stored.
        slurm_error : str
            Path to the directory where the error files should be stored.
        slurm_time : str
            The time limit for the job in the format DD-HH:MM:SS.
        slurm_mem : str
            The memory limit for the job, e.g. 2GB.
        slurm_account : str
            The account to charge the job to. This is usually your username.
        """
        self.slurm_output = slurm_output
        self.slurm_error = slurm_error
        self.slurm_time = slurm_time
        self.slurm_mem = slurm_mem
        self.slurm_account = slurm_account

    def arrayjob(self, encounters: List[Encounter], func: str, name: str = None):
        """Creates an arrayjob that executes a single function on every encounter passed."""
        name = name if name is not None else func
        logging.debug("Creating Arrayjob...")
        logging.debug("Creating pickle files...")
        for e in encounters:
            e.pickle()
        logging.debug("Creating jobscript...")
        template = Template(Path("slurm/array.sh").read_text())
        template = template.substitute({
            "jobname": f"DEA_{name}",
            "outputdir": self.slurm_output,
            "errordir": self.slurm_error,
            "time": self.slurm_time,
            "mem": self.slurm_mem,
            "account": self.slurm_account,
            "loadpythonenv":  "source /hpcwork/jrc_combine/richard/miniconda3/bin/activate dea",
            "root": "/hpcwork/jrc_combine/richard/DEA",
            "eroot": "/hpcwork/jrc_combine/richard/DEA/dea/data/test",
            "array": ",".join([str(e.id) for e in encounters]),
            "func": func,
        })
        logging.debug(f"Running Jobscript {name}")
        Path("jobscript.temp.sh").write_text(template)
        output = subprocess.check_output(["sbatch", "jobscript.temp.sh"])
        logging.debug(output)
        logging.debug("... done")
        return output