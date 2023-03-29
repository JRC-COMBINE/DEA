from __future__ import annotations

import logging
import pandas as pd
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Encounter:
    """Encounter data class.

    This basically stores all relevant information for a single visit of a patient to the hospital.
    You can add more fields if you need them, but make sure to update the save and load methods."""

    id: int
    dynamic: pd.DataFrame
    static: pd.DataFrame
    processed: pd.DataFrame = None

    def __post_init__(self):
        self.preprocess()

    def preprocess(self):
        """Preprocessing is executed at loadtime and should be used to get the data in workable format.
        This includes mostly resampling, filtering and datatype fixing that can not or should not be saved in the source data."""
        self.dynamic.reset_index(inplace=True, drop=True)
        self.dynamic.index = pd.to_timedelta(self.dynamic.index, unit="h")
        self.dynamic = self.dynamic.resample("1h").mean(numeric_only=True)
        self.dynamic.ffill(inplace=True)
        self.dynamic.fillna(-1, inplace=True)
    
    def process(self):
        """This method is called after the cohort is loaded and can be used to calculate additional information.
        This is the place to add your own code."""
        self.processed = self.dynamic.mean()

    def save(self, path: Path):
        """Saves the encounter to disk.
        Extend this methods for every information you want store at the encounter level.
        Usually this method is called through the :meth:`dea.cohort.Cohort.save` method."""
        self.dynamic.to_csv(path / f"dynamic.csv")
        if self.processed is not None:
            self.processed.to_csv(path / f"processed.csv")
    
    @staticmethod
    def from_path(path: Path, static: pd.DataFrame) -> Encounter:
        """Loads the encounter from disk. Reads every csv file in the passed folder and adds it to the encounter."""
        static = static.loc[int(path.stem)]
        processed = None
        for f in path.glob("*.csv"):
            if f.name == "dynamic.csv":
                dynamic = pd.read_csv(f)
            elif f.name == "processed.csv":
                processed = pd.read_csv(f)  # this is just an example, remove or add any files that suit your need
            else:
                logging.warning("Unknown file %s. Implement the loading routine in Encounter.from_path.", f)
        return Encounter(
            id=int(path.stem),
            dynamic=dynamic,
            static=static,
            processed=processed
        )