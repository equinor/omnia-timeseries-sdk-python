"""
Test omnia basic resource
"""
from pandas import DataFrame


def test_repr(new_omnia_resource_a):
    r = repr(new_omnia_resource_a)
    assert isinstance(r, str)
    assert "name" in r
    assert "id" in r


def test_str(new_omnia_resource_a):
    s = str(new_omnia_resource_a)
    assert isinstance(s, str)
    assert "name" in s
    assert "id" in s


def test_dump(new_omnia_resource_a):
    d = new_omnia_resource_a.dump()
    assert isinstance(d, dict)
    assert "name" in d
    assert "id" in d
    assert "external_id" in d


def test_camelcased_dump(new_omnia_resource_a):
    d = new_omnia_resource_a.dump(camel_case=True)
    assert isinstance(d, dict)
    assert "name" in d
    assert "id" in d
    assert "externalId" in d


def test_topandas(new_omnia_resource_a):
    df = new_omnia_resource_a.to_pandas()
    assert isinstance(df, DataFrame)

