import joblib
from dea.cohort import Cohort

if __name__ == "__main__":
    coh = Cohort("/work/jrc_combine/ASIC/kontrolldaten", None, limit_size=100)
    processed = coh.process()
    features = ["Horowitz-Quotient_(ohne_Temp-Korrektur)", "individuelles_Tidalvolumen_pro_kg_idealem_Koerpergewicht", "AF_spontan", "AF", "PEEP", "Compliance", "SpO2", "PCT", "Leukozyten", "paCO2_(ohne_Temp-Korrektur)", "paO2_(ohne_Temp-Korrektur)", "FiO2"]
    states = coh.create_states(4, 8, features)
    joblib.dump(coh, "data/test.joblib")