import unittest
import datetime
from pandas import DataFrame
from omnia_timeseries_sdk import OmniaClient
from omnia_timeseries_sdk.resources import OmniaResource, OmniaResourceList, TimeSeries, TimeSeriesList, DataPoint, \
    DataPoints, DataPointsList


class TimeSeriesListResourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = OmniaClient()
        self.ts = self.client.time_series.retrieve_multiple(["bdc2e4aa-83de-458b-b989-675fa4e58aac",
                                                             "b51e1723-c25b-4847-825e-2da26409ff3c"])

    def tearDown(self) -> None:
        pass

    def test_types(self):
        self.assertIsInstance(self.ts, TimeSeriesList)
        self.assertIsInstance(self.ts.resources, list)
        self.assertIsInstance(self.ts.resources[0], TimeSeries)

    def test_data(self):
        dps = self.ts.data(limit=2)
        self.assertIsInstance(dps, DataPointsList)
        self.assertIsInstance(dps.resources, list)
        self.assertIsInstance(dps.resources[0], DataPoints)

    def test_dump(self):
        d = self.ts.dump()
        self.assertIsInstance(d, list)

    def test_dump_camelcase(self):
        d = self.ts.dump(camel_case=True)
        self.assertIsInstance(d, list)
        self.assertIn("externalId", d[0].keys())

    def test_topandas(self):
        df = self.ts.to_pandas()
        self.assertIsInstance(df, DataFrame)


class TimeSeriesResourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = OmniaClient()
        self.ts = self.client.time_series.retrieve("b51e1723-c25b-4847-825e-2da26409ff3c")

    def tearDown(self) -> None:
        pass

    def test_type(self):
        self.assertIsInstance(self.ts, TimeSeries)

    def test_attributes(self):
        self.assertIsInstance(self.ts.id, str)
        self.assertIsInstance(self.ts.external_id, str)
        self.assertIsInstance(self.ts.name, str)
        self.assertIsInstance(self.ts.description, str)
        self.assertIsInstance(self.ts.step, bool)
        self.assertIsInstance(self.ts.unit, str)
        self.assertIsInstance(self.ts.created_time, datetime.datetime)
        self.assertIsInstance(self.ts.changed_time, datetime.datetime)

    def test_data(self):
        dps = self.ts.data(limit=2)
        self.assertIsInstance(dps, DataPoints)

    def test_dump(self):
        d = self.ts.dump()
        self.assertIsInstance(d, dict)

    def test_dump_camelcase(self):
        d = self.ts.dump(camel_case=True)
        self.assertIn("externalId", d.keys())

    def test_first(self):
        dp = self.ts.first()
        self.assertIsInstance(dp, DataPoint)

    def test_latest(self):
        dp = self.ts.latest()
        self.assertIsInstance(dp, DataPoint)

    def test_topandas(self):
        df = self.ts.to_pandas()
        self.assertIsInstance(df, DataFrame)


class DataPointsListResourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = OmniaClient()
        self.ts = self.client.time_series.retrieve_multiple(["bdc2e4aa-83de-458b-b989-675fa4e58aac",
                                                             "b51e1723-c25b-4847-825e-2da26409ff3c"])
        self.dps = self.ts.data()

    def tearDown(self) -> None:
        pass

    def test_types(self):
        self.assertIsInstance(self.ts, TimeSeriesList)
        self.assertIsInstance(self.dps, DataPointsList)
        self.assertIsInstance(self.dps.resources, list)
        self.assertIsInstance(self.dps.resources[0], DataPoints)

    def test_dump(self):
        d = self.dps.dump()
        self.assertIsInstance(d, list)

    def test_topandas(self):
        df = self.dps.to_pandas()
        self.assertIsInstance(df, DataFrame)


class DataPointsResourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = OmniaClient()
        self.ts = self.client.time_series.retrieve("bdc2e4aa-83de-458b-b989-675fa4e58aac")
        self.dps = self.ts.data()

    def tearDown(self) -> None:
        pass

    def test_types(self):
        self.assertIsInstance(self.ts, TimeSeries)
        self.assertIsInstance(self.dps, DataPoints)
        self.assertIsInstance(self.dps.resources, list)
        self.assertIsInstance(self.dps.resources[0], DataPoint)
        self.assertIsInstance(self.dps.id, str)
        self.assertIsInstance(self.dps.name, str)
        self.assertIsInstance(self.dps.unit, str)
        self.assertIsInstance(self.dps.time, list)
        self.assertIsInstance(self.dps.value, list)
        self.assertIsInstance(self.dps.first, DataPoint)
        self.assertIsInstance(self.dps.latest, DataPoint)

    def test_attributes(self):
        self.assertEqual(self.dps.id, self.ts.id)
        self.assertEqual(self.dps.name, self.ts.name)
        self.assertEqual(self.dps.unit, self.ts.unit)

    def test_dump(self):
        d = self.dps.dump()
        self.assertIsInstance(d, dict)

    def test_topandas(self):
        df = self.dps.to_pandas()
        self.assertIsInstance(df, DataFrame)


class DataPointResourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = OmniaClient()
        self.ts = self.client.time_series.retrieve("bdc2e4aa-83de-458b-b989-675fa4e58aac")
        self.dp = self.ts.first()

    def tearDown(self) -> None:
        pass

    def test_types(self):
        self.assertIsInstance(self.ts, TimeSeries)
        self.assertIsInstance(self.dp, DataPoint)
        self.assertIsInstance(self.dp.id, str)
        self.assertIsInstance(self.dp.name, str)
        self.assertIsInstance(self.dp.unit, str)
        self.assertIsInstance(self.dp.time, datetime.datetime)
        self.assertIsInstance(self.dp.value, (float, int))

    def test_attributes(self):
        self.assertEqual(self.dp.id, self.ts.id)
        self.assertEqual(self.dp.name, self.ts.name)
        self.assertEqual(self.dp.unit, self.ts.unit)

    def test_dump(self):
        d = self.ts.dump()
        self.assertIsInstance(d, dict)

    def test_topandas(self):
        df = self.ts.to_pandas()
        self.assertIsInstance(df, DataFrame)


class OmniaResourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.resource = OmniaResource()
        self.resource.resource_id = "fakepseudorandomid"
        self.resource.name = "theresource"

    def test_repr(self):
        self.assertIsInstance(repr(self.resource), str)
        self.assertIn("name", repr(self.resource))
        self.assertIn("resource_id", repr(self.resource))

    def test_str(self):
        self.assertIsInstance(str(self.resource), str)
        self.assertIn("name", str(self.resource))
        self.assertIn("resource_id", str(self.resource))

    def test_dump(self):
        d = self.resource.dump()
        self.assertIsInstance(d, dict)
        self.assertIn("name", d)
        self.assertIn("resource_id", d)

    def test_cameled_dump(self):
        d = self.resource.dump(camel_case=True)
        self.assertIsInstance(d, dict)
        self.assertIn("name", d)
        self.assertIn("resourceId", d)

    def test_topandas(self):
        df = self.resource.to_pandas()
        self.assertIsInstance(df, DataFrame)


class OmniaResourceListTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.resources = OmniaResourceList()
        r1 = OmniaResource()
        r1.resource_id = "firstid"
        r1.name = "firstresource"
        r2 = OmniaResource()
        r2.resource_id = "secondid"
        r2.name = "secondresource"
        self.resources.resources = [r1, r2]

    def test_repr(self):
        self.assertIsInstance(repr(self.resources), str)
        self.assertIn("name", repr(self.resources))
        self.assertIn("resource_id", repr(self.resources))

    def test_str(self):
        self.assertIsInstance(str(self.resources), str)
        self.assertIn("name", str(self.resources))
        self.assertIn("resource_id", str(self.resources))

    def test_dump(self):
        d = self.resources.dump()
        self.assertIsInstance(d, list)
        self.assertIsInstance(d[0], dict)
        self.assertIn("name", d[0])
        self.assertIn("resource_id", d[0])

    def test_cameled_dump(self):
        d = self.resources.dump(camel_case=True)
        self.assertIsInstance(d, list)
        self.assertIsInstance(d[0], dict)
        self.assertIn("name", d[0])
        self.assertIn("resourceId", d[0])

    def test_topandas(self):
        df = self.resources.to_pandas()
        self.assertIsInstance(df, DataFrame)


if __name__ == '__main__':
    unittest.main()
