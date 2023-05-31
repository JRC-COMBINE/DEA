from __future__ import annotations

import logging
import pandas as pd
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Encounter:
    """Encounter data class.

    This basically stores all relevant information for a single visit of a patient to the hospital.
    You can add more fields if you need them, but make sure to update the save and load methods.
    """

    id: int
    dynamic: pd.DataFrame
    static: pd.DataFrame
    processed: pd.DataFrame
    root: Path

    def __post_init__(self):
        self.preprocess()

    def preprocess(self):
        """Preprocessing is executed at loadtime and should be used to get the data in workable format.
        This includes mostly resampling, filtering and datatype fixing that can not or should not be saved in the source data.
        """
        self.dynamic.reset_index(inplace=True, drop=True)
        self.dynamic = self.dynamic.drop(columns=[c for c in self.dynamic.columns if "Unnamed" in c]) # remove leftover indices from pandas/csv/datetime interaction
        self.dynamic.index = pd.to_timedelta(self.dynamic.index, unit="min")  # assume data is at minutely resolution. Change accordingly!
        self.dynamic.ffill(inplace=True)
        self.dynamic.fillna(-1, inplace=True)

    def delete_extra(self):
        """This method is deletes all but dynamic, static and id."""
        if self.processed is not None:
            Path(self.root / f"processed.csv").unlink()
        self.processed = None

    def process(self):
        """This method is called after the cohort is loaded and can be used to calculate additional information.
        This is the place to add your own code."""
        self.processed = self.dynamic.mean()

    def pickle(self, path: Path = None):
        """Saves the encounter to disk as pickle file. Used for HPC interaction mostly."""
        if path is None and self.root is None:
            raise ValueError(
                "No path specified. Either define during encounter creation, or pass to save method."
            )
        path = path if path is not None else self.root
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        path = path / f"encounter.pkl"
        import joblib

        joblib.dump(self, path)

    def save(self, path: Path = None):
        """Saves the encounter to disk.
        Extend this methods for every information you want store at the encounter level.
        Usually this method is called through the :meth:`dea.cohort.Cohort.save` method.
        """
        if path is None and self.root is None:
            raise ValueError(
                "No path specified. Either define during encounter creation, or pass to save method."
            )
        path = path if path is not None else self.root
        path = Path(path)
        self.dynamic.to_csv(path / f"dynamic.csv")
        if self.processed is not None:
            self.processed.to_csv(path / f"processed.csv")

    @staticmethod
    def from_path_single(payload: tuple[Path, pd.DataFrame]) -> Encounter:
        """Wrapper for the from_path method to be used with multiprocessing."""
        return Encounter.from_path(payload[0], payload[1])

    @staticmethod
    def from_path(path: Path, static: pd.DataFrame) -> Encounter:
        """Loads the encounter from disk. Reads every csv file in the passed folder and adds it to the encounter."""
        static = static.loc[int(path.stem)]
        processed = None
        for f in path.glob("*.csv"):
            try:
                if f.name == "dynamic.csv":
                    dynamic = pd.read_csv(f)
                elif f.name == "processed.csv":
                    processed = pd.read_csv(
                        f
                    )  # this is just an example, remove or add any files that suit your need
                else:
                    logging.warning(
                        "Unknown file %s. Implement the loading routine in Encounter.from_path.",
                        f,
                    )
            except Exception as e:
                logging.error("Could not load %s. %s", f, e)
        return Encounter(
            id=int(path.stem),
            dynamic=dynamic,
            static=static,
            processed=processed,
            root=path,
        )
