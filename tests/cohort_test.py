import pytest
import pandas as pd
from dea.cohort import Cohort


@pytest.fixture()
def c(request):
    return Cohort.from_path("tests/data")

def test_loaded_encounters(c):
    assert c.encounters is not None
    assert len(c.encounters) > 0

def test_loaded_static(c):
    assert c.static is not None
    assert c.static.shape[0] > 0
    assert c.static.shape[1] > 0

def test_processing(c):
    c.process(False)
    assert len(c.processed) > 0