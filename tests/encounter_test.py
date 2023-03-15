import pytest
import numpy as np
import pandas as pd
from dea.encounter import Encounter
from dea.cohort import Cohort

@pytest.fixture
def e():
    return Cohort("control", None, 1).process()[0]

def test_creation(e):
    assert e is not None

def test_validity(e):
    assert e.id is not None
    assert e.source is not None
    assert e.hospital is not None
    assert e.dynamic.shape[0] > 0
    assert e.static.shape[0] > 0
    assert e.comorbidities.shape[0] > 0

def test_to_states(e):
    states = e.to_states(4, 8)
    assert(states is not None)

def test_state_length(e):
    states = e.to_states(4, 8)
    assert len(states) == e.dynamic.shape[0] - (8 + 2*4)  # TODO: verify this

def test_state_example():
    # TODO: assert correct state behavior with toydata
    raise NotImplementedError()