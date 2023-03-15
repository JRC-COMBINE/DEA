import pandas as pd
from dataclasses import dataclass

@dataclass
class Encounter:
    id: int
    source: str
    hospital: int
    dynamic: pd.DataFrame
    static: pd.DataFrame
    comorbidities: pd.DataFrame

    def to_states(self, window_width=4, horizon=8):
        """Calculates the states for the encounter."""
        states = []
        hwc = self.dynamic["Horowitz-Quotient_(ohne_Temp-Korrektur)"]
        for i in range(window_width, len(hwc) - horizon - window_width):
            hw0 = hwc[i - window_width : i]
            hw1 = hwc[i + horizon - 1 : i + horizon + window_width - 1]

            if hw0.isna().all():  # skip the state
                continue

            di = hw0.median() - hw1.median()

            if di == 0:  # skip the state
                label = 0

            if hw0.isna().any() or di == 0:
                label = 1
            elif hw0.mean() > 450 and di > 100:  # we copy label 2
                label = 1
            elif hw0.mean() > 350 and di > 60:
                label = 1
            elif hw0.mean() > 250 and hw1.mean() < 200:
                label = 1
            elif hw0.mean() > 150 and hw1.mean() < 100:
                label = 1
            else:
                label = 0

            s = self.dynamic.iloc[
                i - window_width : i, :
            ].mean()  # drop label (and delta, if it were stored)
            s["label"] = label
            states.append(s)
        return states
