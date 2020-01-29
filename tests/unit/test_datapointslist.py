"""
Test DataPointsList class
"""
from omnia_timeseries_sdk.resources import DataPoints, DataPointsList
from pandas import DataFrame


def test_types(new_datapointslist):
    assert isinstance(new_datapointslist, DataPointsList)
    assert isinstance(new_datapointslist.resources, list)
    assert isinstance(new_datapointslist.resources[0], DataPoints)


def test_len(new_datapointslist):
    assert len(new_datapointslist) == 1


def test_dump(new_datapointslist):
    d = new_datapointslist.dump()
    assert isinstance(d, list)


def test_topandas(new_datapointslist):
    df = new_datapointslist.to_pandas()
    assert isinstance(df, DataFrame)
