"""
Test omnia basic resource list
"""
from pandas import DataFrame


def test_repr(new_omnia_resource_list):
    r = repr(new_omnia_resource_list)
    assert isinstance(r, str)
    assert "name" in r
    assert "id" in r


def test_str(new_omnia_resource_list):
    s = str(new_omnia_resource_list)
    assert isinstance(s, str)
    assert "name" in s
    assert "id" in s


def test_dump(new_omnia_resource_list):
    d = new_omnia_resource_list.dump()
    assert isinstance(d, list)
    assert isinstance(d[0], dict)
    assert "name" in d[0]
    assert "id" in d[0]
    assert "external_id" in d[0]


def test_camelcased_dump(new_omnia_resource_list):
    d = new_omnia_resource_list.dump(camel_case=True)
    assert isinstance(d, list)
    assert isinstance(d[0], dict)
    assert "name" in d[0]
    assert "id" in d[0]
    assert "externalId" in d[0]


def test_topandas(new_omnia_resource_list):
    df = new_omnia_resource_list.to_pandas()
    assert isinstance(df, DataFrame)
