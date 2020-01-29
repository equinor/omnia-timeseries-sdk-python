"""
Test general stuff
"""
import omnia_timeseries_sdk


def test_version():
    assert isinstance(omnia_timeseries_sdk.__version__, str)

