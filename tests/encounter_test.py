import pytest
import numpy as np
import pandas as pd
from dea.encounter import Encounter
from dea.cohort import Cohort

@pytest.fixture
def e():
    return Cohort.from_path("tests/data").encounters[0]

def test_exists(e):
    assert e is not None

def test_validity(e):
    assert e.id is not None
    assert e.dynamic is not None
    assert e.static is not None
    assert e.processed is None
    assert e.root is not None
    assert e.dynamic.shape[0] > 0
    assert e.static.shape[0] > 0

def test_process(e):
    e.process()
    assert(e.processed is not None)