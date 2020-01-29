"""
Test TimeSeries class
"""
from pandas import DataFrame
from omnia_timeseries_sdk.resources import TimeSeries, TimeSeriesList


def test_types(new_timeserieslist):
    assert isinstance(new_timeserieslist, TimeSeriesList)
    assert isinstance(new_timeserieslist.resources, list)
    assert isinstance(new_timeserieslist.resources[0], TimeSeries)


def test_len(new_timeserieslist):
    assert len(new_timeserieslist) == 1


def test_dump(new_timeserieslist):
    d = new_timeserieslist.dump()
    assert isinstance(d, list)
    assert "external_id" in d[0]


def test_camelcased_dump(new_timeserieslist):
    d = new_timeserieslist.dump(camel_case=True)
    assert isinstance(d, list)
    assert "externalId" in d[0]     # keys()?


def test_topandas(new_timeserieslist):
    df = new_timeserieslist.to_pandas()
    assert isinstance(df, DataFrame)

