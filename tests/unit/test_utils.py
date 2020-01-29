"""
Test utility functions
"""
from omnia_timeseries_sdk._utils import from_datetime_string, to_omnia_datetime_string, to_camel_case, to_snake_case


def test_snake_dict(data):
    """Assert that keys in data container are correctly converted to snake case."""
    d = to_snake_case(data)
    d2 = d.get("data")[0]   # need only one
    assert "asset_id" in d
    assert "external_id" in d
    assert "name" in d
    assert "data" in d
    assert "sub_asset_id" in d2
    assert "created_time" in d2


def test_snake_str():
    assert "some_camel_cased_string" == to_snake_case("someCamelCasedString")


def test_camel_dict(data):
    """Assert that keys in data container are correctly converted to camel case."""
    d = to_camel_case(to_snake_case(data))
    d2 = d.get("data")[0]   # need only one
    assert "assetId" in d
    assert "externalId" in d
    assert "name" in d
    assert "data" in d
    assert "subAssetId" in d2
    assert "createdTime" in d2


def test_datetime_strings():
    s = "2008-09-03T20:56:35.450686Z"
    assert s == to_omnia_datetime_string(from_datetime_string("2008-09-03T20:56:35.450686Z"))
    assert s == to_omnia_datetime_string(from_datetime_string("2008-09-03T20:56:35.450686+00:00"))

