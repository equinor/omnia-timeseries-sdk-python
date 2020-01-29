"""
Test DataPoints class
"""
from omnia_timeseries_sdk.resources import DataPoint, DataPoints
from pandas import DataFrame


def test_types(new_datapoints):
    assert isinstance(new_datapoints, DataPoints)
    assert isinstance(new_datapoints.id, str)
    assert isinstance(new_datapoints.name, str)
    assert isinstance(new_datapoints.unit, str)
    assert isinstance(new_datapoints.time, list)
    assert isinstance(new_datapoints.value, list)
    assert isinstance(new_datapoints.resources, list)
    assert isinstance(new_datapoints.resources[0], DataPoint)
    assert isinstance(new_datapoints.first, DataPoint)
    assert isinstance(new_datapoints.latest, DataPoint)


def test_attributes(new_datapoints):
    assert new_datapoints.id == new_datapoints.first.id
    assert new_datapoints.name == new_datapoints.first.name
    assert new_datapoints.unit == new_datapoints.first.unit


def test_len(new_datapoints):
    assert len(new_datapoints) == 2


def test_dump(new_datapoints):
    d = new_datapoints.dump()
    assert isinstance(d, dict)


def test_topandas(new_datapoints):
    df = new_datapoints.to_pandas()
    assert isinstance(df, DataFrame)

