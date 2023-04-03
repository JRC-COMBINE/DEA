from dea.cohort import Cohort
coh = Cohort.from_path("tests/data")
coh.save("dea/data/test")
