import logging
import numpy as np
import pandas as pd
import itertools
from multiprocessing import Pool, cpu_count
from typing import List, Tuple
from pathlib import Path
from rich.progress import track
from configparser import ConfigParser
from dea.encounter import Encounter

class Cohort:
    """Cohort class encompasses multiple encounters.."""

    def __init__(self, path: str, filter_hospitals: List[int] = None, limit_size: int = None, required_los: pd.Timedelta = None) -> None:
        self.path = path
        self.limit_size = limit_size
        if limit_size is not None:
            logging.warning("Limiting size to loading only %d encounters!", limit_size)
        self.required_los = required_los
        if required_los is not None:
            logging.warning("Limiting to encounters with a minimum length of stay of %s!", required_los)
        self.filter_hospitals = filter_hospitals
        if self.filter_hospitals is not None and len(self.filter_hospitals) == 0:
            self.filter_hospitals = None
        self.dynamic, self.static, self.comorbidities = self.load_data()
        self.processed = []
        self.states = {}  # type: Dict[(int, int), List[pd.DataFrame]] for caching 

    def read_config(self, config_file: str) -> ConfigParser:
        """Reads the config file containing paths to various data sources"""
        config = ConfigParser()
        config.read(config_file)
        logging.debug("Read config file %s", config_file)
        logging.debug("Possible data paths: %s", config.items("paths"))
        return config

    def filter(self, encounter_ids: List[int]):
        """CopyConstuctor with encounter_ids to filter"""
        coh = Cohort(self.path, self.filter_hospitals, self.limit_size)
        coh.dynamic = [d for d in self.dynamic if int(d.stem) in encounter_ids]
        coh.processed = [e for e in self.processed if e.id in encounter_ids]
        return coh

    def create_states_multiprocess(self, payload: Tuple[List[str],int,int]) -> pd.DataFrame:
        """Multiprocessing wrapper for Encounter.to_states"""
        d, window_width, horizon = payload
        return d.to_states(window_width, horizon)

    def create_states(self, window_width: int, horizon: int, features: List[str]) -> pd.DataFrame:
        logging.info("reducing to ards relevant parameters...")
        if self.processed is None:
            raise ValueError("No data loaded yet! Call process() first!")
        if str((window_width, horizon)) in self.states:
            logging.info("Using cached states")
            return self.states[str((window_width, horizon))]
        else:
            tempdata = self.processed.copy()
            for d in tempdata:
                d.dynamic = d.dynamic[features]
                d.dynamic = d.dynamic.reindex(sorted(features), axis=1)  # important for some models
                assert(d.dynamic.shape[1] == len(features))

            logging.info("Generating States for %d encounters...", len(tempdata))
            payload = [(d, window_width, horizon) for d in tempdata]
            with Pool(cpu_count()) as p:
                states = list(p.imap(self.create_states_multiprocess, payload))
            states = [s for s in itertools.chain(*states)]
            states = pd.concat(states, axis=1).T
            for c in states.columns:
                if (states[c] == -1).all():
                    logging.warning("Dropping column %s with only -1 charted!", c)
                    states.drop(c, axis=1, inplace=True)
            states = states.replace(-1, np.NaN).dropna()  # matlab reads -1 as NaN
            states = states.reset_index(drop=True)
            states.label = states.label.astype(bool)
            self.states[str((window_width, horizon))] = states
        return states

    def process(self):
        """Actually reads the data and creates Encounters."""
        logging.info("starting parallel processing")
        with Pool(cpu_count()) as p:
            processed = list(
                track(
                    p.imap(self.process_single, self.dynamic), total=len(self.dynamic)
                )
            )
        bad_returns = 0
        for p in processed:
            if p is not None:
                self.processed.append(p)
            else:
                bad_returns += 1
        logging.warning(f"Skipped {bad_returns} out of {len(self.dynamic)} encounters")
        logging.info("Finished processing")
        return self.processed

    def process_single(self, f: Path) -> Encounter:
        """To be used with multiprocessing. Adds SL if available, labels ards and resamples. returns an Encounter object"""
        df = pd.read_csv(f, low_memory=False)
        df = self.preprocess(df)
        if len(df) == 0:
            logging.debug("No data in %s. Skipping ...", f)
            return None
        if self.required_los is not None and df.index[-1] < self.required_los:
            logging.debug("Encounter %s too short. Skipping ...", f)
            return None
        eid = int(f.stem)
        hid = f.parent.parent.stem
        try:
            return Encounter(eid, self.path, hid, df, self.static[hid].loc[eid], self.comorbidities[hid].loc[eid])
        except KeyError:
            logging.warning("No static data and/or comorbidities for %s", f)
            return Encounter(eid, self.path, hid, df, None, None)
    
    def save(self, fname: str):
        """Saves the processed data to a pickle file"""
        import joblib
        joblib.dump(self, fname)

    def load_files(self, dir, glob):
        """Loads files from a directory. Returns a list of paths."""
        files = []
        logging.info("Loading file list ...")
        for f in Path(dir).rglob(glob):
            if self.filter_hospitals is None or int(f.parent.parent.stem.split("_")[-1]) in self.filter_hospitals:
                files.append(f)
            if self.limit_size is not None and len(files) >= self.limit_size:
                break
        logging.info(f"Loaded {len(files)} files\tFilter: [{self.filter_hospitals}]")
        return files

    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Loads the data from the source and returns a tuple of dynamic and static data"""
        logging.debug("Loading data from %s", self.path)
        dynamic = self.load_files(self.path, "dynamic/*.csv")
        print(self.path)
        static = {}
        for f in (Path(self.path) / "features").rglob("personal.xlsx"):
            static[f.parent.stem] = pd.read_excel(f)

        comorbidities = {}
        for f in (Path(self.path)/"features").rglob("*comorbidities.xlsx"):
            if self.filter_hospitals is None or int(f.parent.stem.split("_")[-1]) in self.filter_hospitals:
                comorbidities[f.parent.stem] = pd.read_excel(f)
                if "encounterid" in comorbidities[f.parent.stem].columns:
                    comorbidities[f.parent.stem].set_index("encounterid", inplace=True)
        return dynamic, static, comorbidities

    @staticmethod
    def preprocess(df, resample=None):
        """Preprocesses the data by removing unnecessary columns and resampling the data"""
        df.index = pd.to_timedelta(df.index, unit="m")
        if resample is not None:
            df = df.resample(resample).mean()
        df.ffill(inplace=True)
        df.fillna(-1, inplace=True)
        return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    coh = Cohort("control", None, limit_size=100)
    processed = coh.process()
    features = ["Horowitz-Quotient_(ohne_Temp-Korrektur)", "individuelles_Tidalvolumen_pro_kg_idealem_Koerpergewicht", "AF_spontan", "AF", "PEEP", "Compliance", "SpO2", "PCT", "Leukozyten", "paCO2_(ohne_Temp-Korrektur)", "paO2_(ohne_Temp-Korrektur)", "FiO2"]
    states = coh.create_states(4, 8, features)
    print(len(coh.processed))
    print(len(states))
