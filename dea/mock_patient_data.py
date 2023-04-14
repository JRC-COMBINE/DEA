#!/usr/bin/python
# -*- coding: utf-8 -*-

# This script generates mock patient data for testing purposes. It is not intended to be used in production.
# It is based on the synthetic data generation through DoppelgangerGAN (DGAN) from Gretel AI.

import joblib
import random
from collections import defaultdict
import pandas as pd
from gretel_synthetics.timeseries_dgan.dgan import DGAN
from gretel_synthetics.timeseries_dgan.config import DGANConfig
from matplotlib import pyplot as plt

if __name__ == "__main__":
    print("loading data")
    coh = joblib.load(
        "data/mock.joblib"
    )  # this is a cohort to sample from for test data generation
    print("data loaded")

    data = defaultdict(list)

    for p in coh.processed:
        for c in p.dynamic.columns:
            data[c].append(p.dynamic[c])

    for k, v in data.items():
        data[k] = pd.concat(v)

    data = pd.DataFrame(data)

    model = DGAN(
        DGANConfig(
            max_sequence_len=36,
            sample_len=9,
            batch_size=1000,
            epochs=300,
            cuda=True,
        )
    )

    model.train_dataframe(
        data,
        df_style="long",
    )

    # Generate synthetic data
    for i in range(100):
        simulated = model.generate_dataframe(200)
        end_of_stay = random.randint(100, len(simulated - 1))
        simulated = simulated.iloc[:end_of_stay, :]
        simulated.index = pd.TimedeltaIndex(simulated.index, unit="h")
        simulated.to_csv(f"../tests/data/{i}/dynamic.csv")
