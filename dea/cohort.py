from __future__ import annotations
import logging
import pandas as pd
from typing import List
from pathlib import Path
from dea.encounter import Encounter

class Cohort:
    """Cohort class encompasses multiple encounters.."""

    def __init__(self):
        """Initializes the cohort."""
        self.encounters: List[Encounter] = []
        self.static: pd.DataFrame = None
    
    def get_processed(self) -> pd.DataFrame:
        """Returns all encounters that have already been processed."""
        return [e.processed for e in self.encounters if e.processed is not None]

    @staticmethod
    def from_path(path: str) -> Cohort:
        """Loads the data from the source and stores all information found."""
        logging.debug("Loading cohort from %s", path)
        cohort = Cohort()
        cohort.encounters = []
        cohort.static = pd.read_csv(path+"/static.csv")
        for subdir in Path(path).rglob("*"):  # todo parallelize
            if subdir.is_dir():
                cohort.encounters.append(Encounter.from_path(subdir, cohort.static))
            else:
                pass # load other cohort level information here
        return cohort
    
    def process(self):
        """This methods executes :meth:`dea.encounter.Encounter.process` on all encounters in the cohort."""
        logging.debug("Processing cohort ...")
        for e in self.encounters:
            e.process()
    
    def save(self, path: str):
        """Saves the cohort to csv folder structure.
        Extend this method for every information you want store at the encounter level.
        This method additionally calls :meth:`dea.encounter.Encounter.save` on every encounter in the cohort."""
        logging.debug("Saving cohort ...")
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        self.static.to_csv(path/"static.csv")
        for e in self.encounters:  # todo: parallelize
            Path(path/str(e.id)).mkdir(parents=True, exist_ok=True)
            e.save(Path(path) / str(e.id))

    def preprocess(self):
        """Executes preprocessing on all Encounters in the cohort.
        Extend this method for preprocessing that requires cohort-level information, or use :meth:`dea.encounter.Encounter.preprocess`.
        This method additionally calls :meth:`dea.encounter.Encounter.preprocess` on every encounter in the cohort."""
        logging.debug("Preprocessing cohort ...")
        for e in self.encounters:  # todo: parallelize
            e.preprocess()
