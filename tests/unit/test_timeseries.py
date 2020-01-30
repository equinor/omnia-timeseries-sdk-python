"""
Test TimeSeries class
"""
from datetime import datetime
from pandas import DataFrame
from omnia_timeseries_sdk.resources import TimeSeries, TimeSeriesList


def test_types(new_timeseries):
    assert isinstance(new_timeseries, TimeSeries)
    assert isinstance(new_timeseries.id, str)
    assert isinstance(new_timeseries.external_id, str)
    assert isinstance(new_timeseries.asset_id, str)
    assert isinstance(new_timeseries.name, str)
    assert isinstance(new_timeseries.description, str)
    assert isinstance(new_timeseries.step, bool)
    assert isinstance(new_timeseries.unit, str)
    assert isinstance(new_timeseries.created_time, datetime)
    assert isinstance(new_timeseries.changed_time, datetime)


def test_dump(new_timeseries):
    d = new_timeseries.dump()
    assert isinstance(d, dict)
    assert "external_id" in d


def test_camelcased_dump(new_timeseries):
    d = new_timeseries.dump(camel_case=True)
    assert isinstance(d, dict)
    assert "externalId" in d


def test_topandas(new_timeseries):
    df = new_timeseries.to_pandas()
    assert isinstance(df, DataFrame)

