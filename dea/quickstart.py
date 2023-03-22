from dea.cohort import Cohort
coh = Cohort("../tests/data")
coh.process()
coh.save("data/test.joblib")
