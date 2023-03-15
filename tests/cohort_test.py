import pytest
import pandas as pd
from dea.cohort import Cohort


@pytest.fixture(params=["calibration", "control"])
def c(request):
    return Cohort(request.param, None, limit_size=100)


def test_config(c):
    assert c.config is not None


def test_loaded_dynamic(c):
    assert c.dynamic is not None
    assert len(c.dynamic) > 0

def test_comorbidities(c):
    assert c.comorbidities is not None
    assert len(c.comorbidities) > 0
    assert(isinstance(c.comorbidities, dict))

def test_loaded_static(c):
    assert c.static is not None
    assert len(c.static) > 0


def disabled_test_loaded_all_dynamic(dl): # Disabled because limit_size=100
    if dl.source == "calibration":
        assert len(c.dynamic) == 43381  # 19-01-2023
    elif c.source == "control":
        assert len(c.dynamic) == 28886  # 19-01-2023
    else:
        raise ValueError("Unknown soure %s" % c.source)


def test_loaded_all_static(c):
    if c.source == "calibration":
        assert (
            len(c.static) == 5
        )  # Should be [0, 1, 2, 3, 5, 7], but only [0, 1, 2, 3, 5] provide static data  (19-01-2023)
    elif c.source == "control":
        assert (
            len(c.static) == 6
        )  # Should be [0, 2, 3, 4, 7, 8, 9], but hospital 4 does not provide static data  (19-01-2023)
    else:
        raise ValueError("Unknown soure %s" % c.source)

def test_loeded_comorbidities(c):
    assert c.comorbidities is not None
    assert len(c.comorbidities.keys()) > 0
    if c.source == "calibration":
        assert len(c.comorbidities.keys()) == 5
    elif c.source == "control":
        assert len(c.comorbidities.keys()) == 6
    else:
        raise ValueError("Unknown soure %s" % c.source)

def test_processing(c):
    c.process()
    assert len(c.processed) > 0

def test_filtering():
    c = Cohort("control", [0], limit_size=100)
    assert(c.filter_hospitals == [0])
    assert(isinstance(c.comorbidities, dict))