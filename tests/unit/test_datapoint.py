"""
Test DataPoint class
"""
from datetime import datetime
from omnia_timeseries_sdk.resources import DataPoint
from pandas import DataFrame


def test_types(new_datapoint):
    assert isinstance(new_datapoint, DataPoint)
    assert isinstance(new_datapoint.id, str)
    assert isinstance(new_datapoint.name, str)
    assert isinstance(new_datapoint.unit, str)
    assert isinstance(new_datapoint.time, datetime)
    assert isinstance(new_datapoint.value, (float, int))


def test_attributes(new_datapoint):
    assert new_datapoint.id == "someid"
    assert new_datapoint.name == "ameasure"
    assert new_datapoint.unit == "m"


def test_dump(new_datapoint):
    d = new_datapoint.dump()
    assert isinstance(d, dict)


def test_topandas(new_datapoint):
    df = new_datapoint.to_pandas()
    assert isinstance(df, DataFrame)
