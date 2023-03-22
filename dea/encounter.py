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

    def __post_init__(self):
        self.preprocess()

    def preprocess(self):
        """Preprocessing is executed at loadtime and should be used to get the data in workable format.
        This includes mostly resampling, filtering and datatype fixing that can not or should not be saved in the source data."""
        self.dynamic.reset_index(inplace=True)
        self.dynamic.index = pd.to_timedelta(self.dynamic.index, unit="m")
        self.dynamic = self.dynamic.resample("1h").mean(numeric_only=True)
        self.dynamic.ffill(inplace=True)
        self.dynamic.fillna(-1, inplace=True)

    def save(self, path):
        """Saves the encounter to disk.
        Extend this methods for every information you want store at the encounter level.
        Usually this method is called through the :meth:`dea.cohort.Cohort.save` method."""
        self.dynamic.to_csv(path / f"dynamic.csv")
    
    @staticmethod
    def from_path(path: Path, static: pd.DataFrame) -> Encounter:
        """Loads the encounter from disk. Reads every csv file in the passed folder and adds it to the encounter."""
        for f in path.glob("*.csv"):
            if f.name == "dynamic.csv":
                dynamic = pd.read_csv(f)
            else:
                logging.warning("Unknown file %s. Implement the loading routine in Encounter.from_path.", f)
        return Encounter(int(path.stem), dynamic, static.loc[int(path.stem)])