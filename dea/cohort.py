from __future__ import annotations
import logging
import pandas as pd
from rich.progress import track
from multiprocessing import Pool, cpu_count
from typing import List
from pathlib import Path
from dea.encounter import Encounter


class Cohort:
    """Cohort class encompasses multiple encounters.."""

    def __init__(self, root: Path = None, hpc_bridge=None):
        """Initializes the cohort."""
        self.encounters: List[Encounter] = []
        self.static: pd.DataFrame = None
        self.root = root
        self.hpc_bridge = hpc_bridge

    @property
    def processed(self):
        return self.get_processed()
    
    def to_pandas(self) -> pd.DataFrame: # TODO: Implement Tests and version that adds static information at every timestep
        """Returns a concatenated dataframe of the dynamic data of all encounters."""
        return pd.concat([e.dynamic for e in self.encounters])

    def get_processed(self) -> pd.DataFrame:
        """Returns all encounters that have already been processed."""
        return [e.processed for e in self.encounters if e.processed is not None]

    @staticmethod
    def from_path(path: str, hpc_bridge=None) -> Cohort:
        """Loads the data from the source and stores all information found."""
        logging.debug("Loading cohort from %s", path)
        cohort = Cohort()
        cohort.hpc_bridge = hpc_bridge
        cohort.encounters = []
        cohort.root = path
        cohort.static = pd.read_csv(path + "/static.csv")
        dynamic_files = [f for f in Path(path).rglob("*") if f.is_dir()]
        with Pool(cpu_count()) as p:
            cohort.encounters = list(
                track(
                    p.imap(
                        Encounter.from_path_single,
                        [(f, cohort.static) for f in dynamic_files],
                    ),
                    description="Loading dynamic encounters",
                    total=len(dynamic_files),
                )
            )
        return cohort

    def process(self, safe: bool = True):
        """This methods executes :meth:`dea.encounter.Encounter.process` on all encounters in the cohort.
        If a hpc_bridge is defined, it will be used to query the jobs for HPC.
        Returns a message for the DEA Interface to be displayed.
        """
        logging.debug("Processing cohort ...")
        if self.hpc_bridge is None:
            for e in self.encounters:  # TODO: Parallelize
                e.process()
            if safe:
                self.save()
            return "Cohort Processed."
        else:
            msg = self.hpc_bridge.arrayjob(self.encounters, "process")
            return msg
            # return "Processing queued with HPC Controller. Refresh (top menu) to check for results!"

    def delete_extra(self):
        """This method deletes all extra information from the encounters."""
        logging.debug("Deleting extra data from encounters ...")
        for e in self.encounters:
            e.delete_extra()
        # also clean up additional files you created on cohort level here

    def save(self, path: str = None):
        """Saves the cohort to csv folder structure.
        Extend this method for every information you want store at the encounter level.
        This method additionally calls :meth:`dea.encounter.Encounter.save` on every encounter in the cohort.
        """
        logging.debug("Saving cohort ...")
        if path is None and self.root is None:
            raise ValueError(
                "No path specified. Either define during cohort creation, or pass to save method."
            )
        path = path if path is not None else self.root
        path = path
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        self.static.to_csv(path / "static.csv")
        for e in self.encounters:
            Path(path / str(e.id)).mkdir(parents=True, exist_ok=True)
            e.save(Path(path) / str(e.id))

    def preprocess(self):
        """Executes preprocessing on all Encounters in the cohort.
        Extend this method for preprocessing that requires cohort-level information, or use :meth:`dea.encounter.Encounter.preprocess`.
        This method additionally calls :meth:`dea.encounter.Encounter.preprocess` on every encounter in the cohort.
        """
        logging.debug("Preprocessing cohort ...")
        for e in self.encounters:  # todo: parallelize
            e.preprocess()
