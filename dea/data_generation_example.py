import joblib
from dea_tools.data.dataloader import DataLoader

if __name__ == "__main__":
    dl = DataLoader("control", None, limit_size=100)
    processed = dl.process()
    features = ["Horowitz-Quotient_(ohne_Temp-Korrektur)", "individuelles_Tidalvolumen_pro_kg_idealem_Koerpergewicht", "AF_spontan", "AF", "PEEP", "Compliance", "SpO2", "PCT", "Leukozyten", "paCO2_(ohne_Temp-Korrektur)", "paO2_(ohne_Temp-Korrektur)", "FiO2"]
    states = dl.create_states(4, 8, features)
    joblib.dump(dl, "data/test.joblib")