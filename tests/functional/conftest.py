"""
Configure integration tests
"""
import pytest
from omnia_timeseries_sdk import OmniaClient
from omnia_timeseries_sdk._config import TestConfig
from omnia_timeseries_sdk.exceptions import OmniaTimeSeriesAPIError
from datetime import datetime, timedelta, timezone


@pytest.fixture(scope="module")
def client():
    """Expose an Omnia API client configured for testing."""
    client = OmniaClient(config=TestConfig)
    return client


@pytest.fixture(scope="module")
def new_timeseries(client):
    """Create a data set for testing."""
    # create data set
    ts = client.time_series.create(
        "PYSDK_TEST_SERIES",
        description="Time series instance created for testing API.",
        unit="horse"
    )
    t0 = datetime(2020, 1, 1, hour=12, minute=0, second=0, tzinfo=timezone.utc)
    dt = timedelta(days=1)
    ts.add_data([t0, t0 + dt, t0 + 2 * dt], [100, 200, 150], [0, 0, 0])

    # yield data
    yield ts

    # clean up
    try:
        ts.delete_data()
    except OmniaTimeSeriesAPIError:
        pass

    ts.delete()
