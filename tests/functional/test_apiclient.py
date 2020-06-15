import pytest
from datetime import datetime, timedelta, timezone
from omnia_timeseries_sdk.resources import TimeSeries, TimeSeriesList, DataPoint, DataPoints


# @pytest.mark.integrationtest
# def test_list(client, new_timeseries):
#     tsl = client.time_series.list()
#     assert isinstance(tsl, TimeSeriesList)
#     assert len(tsl) == 1
#
#
# @pytest.mark.integrationtest
# def test_list_name(client, new_timeseries):
#     tsl = client.time_series.list(name="PYSDK_")
#     assert isinstance(tsl, TimeSeriesList)
#     assert len(tsl) == 1
#     assert isinstance(tsl.resources[0], TimeSeries)


@pytest.mark.integrationtest
def test_retrieve(client, new_timeseries):
    ts = client.time_series.retrieve(new_timeseries.id)
    assert isinstance(ts, TimeSeries)
    assert ts.name == new_timeseries.name
    assert ts.description == new_timeseries.description
    assert ts.unit == new_timeseries.unit
    assert ts.asset_id is None
    assert ts.external_id is None
    assert ts.facility is None
    assert not ts.step


@pytest.mark.integrationtest
def test_retrieve_multiple(client, new_timeseries):
    tsl = client.time_series.retrieve_multiple([new_timeseries.id])
    ts = tsl.resources[0]
    assert isinstance(tsl, TimeSeriesList)
    assert len(tsl) == 1
    assert isinstance(ts, TimeSeries)
    assert ts.name == new_timeseries.name
    assert ts.description == new_timeseries.description
    assert ts.unit == new_timeseries.unit
    assert ts.asset_id is None
    assert ts.external_id is None
    assert ts.facility is None
    assert not ts.step


@pytest.mark.integrationtest
def test_update(client, new_timeseries):
    new_timeseries.update(unit="donkey")
    ts = client.time_series.retrieve(new_timeseries.id)
    assert isinstance(ts, TimeSeries)
    assert ts.name == new_timeseries.name
    assert ts.description == new_timeseries.description
    assert ts.unit == "donkey"
    assert ts.asset_id is None
    assert ts.external_id is None
    assert not ts.step


@pytest.mark.integrationtest
def test_first_dp(new_timeseries):
    dp = new_timeseries.first()
    assert isinstance(dp, DataPoint)
    assert isinstance(dp.time, datetime)
    assert isinstance(dp.value, (int, float))
    assert isinstance(dp.status, int)
    assert isinstance(dp.unit, str)
    assert dp.value == 100
    assert dp.time == datetime(2020, 1, 1, hour=12, minute=0, second=0, tzinfo=timezone.utc)


@pytest.mark.integrationtest
def test_latest_dp(new_timeseries):
    dp = new_timeseries.latest()
    assert isinstance(dp, DataPoint)
    assert isinstance(dp.time, datetime)
    assert isinstance(dp.value, (int, float))
    assert isinstance(dp.status, int)
    assert isinstance(dp.unit, str)
    assert dp.value == 150
    assert dp.time == datetime(2020, 1, 3, hour=12, minute=0, second=0, tzinfo=timezone.utc)


@pytest.mark.integrationtest
def test_dps_in_twin(new_timeseries):
    start = datetime(2020, 1, 1, hour=12, minute=0, second=0, tzinfo=timezone.utc) - timedelta(days=1)
    end = datetime(2020, 1, 1, hour=12, minute=0, second=0, tzinfo=timezone.utc) + timedelta(days=1.5)
    dps = new_timeseries.data(start_time=start.isoformat(), end_time=end.isoformat())
    assert isinstance(dps, DataPoints)
    assert len(dps) == 2
    assert dps.id == new_timeseries.id
    assert dps.value == [100, 200]
    for dp in dps:
        assert isinstance(dp, DataPoint)
        assert dp.time >= start
        assert dp.time <= end


@pytest.mark.integrationtest
def test_dps_after_time(new_timeseries):
    start = datetime(2020, 1, 1, hour=12, minute=0, second=0, tzinfo=timezone.utc) + timedelta(hours=12)
    dps = new_timeseries.data(start_time=start.isoformat())
    assert isinstance(dps, DataPoints)
    assert len(dps) == 2
    assert dps.id == new_timeseries.id
    assert dps.value == [200, 150]
    for dp in dps:
        assert isinstance(dp, DataPoint)
        assert dp.time >= start


@pytest.mark.integrationtest
def test_include_outside_dps(new_timeseries):
    start = datetime(2020, 1, 1, hour=12, minute=0, second=0, tzinfo=timezone.utc) + timedelta(hours=12)
    dps = new_timeseries.data(start_time=start.isoformat(), include_outside_points=True)
    assert isinstance(dps, DataPoints)
    assert len(dps) == 3
    assert dps.id == new_timeseries.id
    assert dps.value == [100, 200, 150]
    for dp in dps:
        assert isinstance(dp, DataPoint)

