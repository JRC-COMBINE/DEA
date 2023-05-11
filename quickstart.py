from dea.cohort import Cohort

if __name__ == "__main__":
    coh = Cohort.from_path("tests/data")
    coh.save("dea/data/test")
