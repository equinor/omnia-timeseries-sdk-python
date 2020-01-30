"""
Configure unit tests
"""
import pytest
from datetime import datetime, timedelta, timezone
from omnia_timeseries_sdk.resources import OmniaResource, OmniaResourceList, TimeSeries, TimeSeriesList, DataPoint, \
    DataPoints, DataPointsList


@pytest.fixture(scope="module")
def data():
    data = dict(assetId="hldhaf645",
                name="something",
                externalId="ad646d7fad1fa6d84f6",
                data=[
                    dict(subAssetId="ad684fa", createdTime=datetime.utcnow()),
                    dict(subAssetId="qw77wtg", createdTime=datetime.utcnow()),
                ])
    return data


@pytest.fixture(scope="module")
def new_omnia_resource_a():
    r = OmniaResource()
    r.id = "a"
    r.name = "bruce"
    r.external_id = "batman"
    return r


@pytest.fixture(scope="module")
def new_omnia_resource_b():
    r = OmniaResource()
    r.id = "b"
    r.name = "dontremember"
    r.external_id = "robin"
    return r


@pytest.fixture(scope="module")
def new_omnia_resource_list(new_omnia_resource_a, new_omnia_resource_b):
    rl = OmniaResourceList()
    rl.resources = [new_omnia_resource_a, new_omnia_resource_b]
    return rl


@pytest.fixture(scope="module")
def new_datapoint():
    dp = DataPoint(
        id="someid",
        name="ameasure",
        unit="m",
        time=datetime.now(tz=timezone.utc).isoformat(),
        value=100.,
        status=0
    )
    return dp


@pytest.fixture(scope="module")
def new_datapoints(new_datapoint):
    dps = DataPoints(
        id=new_datapoint.id,
        name=new_datapoint.name,
        unit=new_datapoint.unit,
        time=[new_datapoint.time.isoformat(), (new_datapoint.time + timedelta(days=1)).isoformat()],
        value=[new_datapoint.value, new_datapoint.value + 100.])
    return dps


@pytest.fixture(scope="module")
def new_datapointslist(new_datapoints):
    return DataPointsList([new_datapoints])


@pytest.fixture(scope="module")
def new_timeseries():
    ts = TimeSeries(
        id="ab12-6addk-dafa",
        name="ameasure",
        unit="m",
        external_id="K67-R",
        description="for testing",
        asset_id="K67",
        created_time=datetime.now(tz=timezone.utc).isoformat(),
        changed_time=datetime.now(tz=timezone.utc).isoformat(),
    )
    return ts


@pytest.fixture(scope="module")
def new_timeserieslist(new_timeseries):
    return TimeSeriesList([new_timeseries])

