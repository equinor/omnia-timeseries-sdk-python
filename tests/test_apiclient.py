import unittest
import datetime
from omnia_timeseries_sdk import OmniaClient
from omnia_timeseries_sdk.resources import TimeSeries, TimeSeriesList, DataPoint, DataPoints


class OmniaTimeSeriesAPITestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = OmniaClient()

    def tearDown(self) -> None:
        pass

    def test_data_with_limit(self):
        end = datetime.datetime(2019, 11, 20, hour=12, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
        start = end - datetime.timedelta(hours=1)
        dps = self.client.time_series.data("b51e1723-c25b-4847-825e-2da26409ff3c", limit=10, start=start.isoformat(),
                                           end=end.isoformat())
        self.assertIsInstance(dps, DataPoints)
        self.assertEqual(len(dps), 10)
        self.assertIsInstance(dps.resources[0], DataPoint)

    def test_data(self):
        dps = self.client.time_series.data("b51e1723-c25b-4847-825e-2da26409ff3c")
        self.assertIsInstance(dps, DataPoints)
        self.assertIsInstance(dps.resources[0], DataPoint)
        self.assertIsInstance(dps.resources[-1], DataPoint)
        self.assertLessEqual(datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1), dps.resources[0].time)
        self.assertLessEqual(dps.resources[-1].time, datetime.datetime.now(tz=datetime.timezone.utc))

    def test_data_with_twin(self):
        end = datetime.datetime(2019, 11, 20, hour=12, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
        start = end - datetime.timedelta(hours=1)
        dps = self.client.time_series.data("b51e1723-c25b-4847-825e-2da26409ff3c", start=start.isoformat(),
                                           end=end.isoformat())
        self.assertIsInstance(dps, DataPoints)
        self.assertIsInstance(dps.resources[0], DataPoint)
        self.assertIsInstance(dps.resources[-1], DataPoint)
        self.assertLessEqual(start, dps.resources[0].time)
        self.assertLessEqual(dps.resources[-1].time, end)

    def test_data_with_twin_including_outside_points(self):
        end = datetime.datetime(2019, 11, 20, hour=12, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
        start = end - datetime.timedelta(hours=1)
        dps = self.client.time_series.data("b51e1723-c25b-4847-825e-2da26409ff3c", start=start.isoformat(),
                                           end=end.isoformat(), include_outside_points=True)
        self.assertIsInstance(dps, DataPoints)
        self.assertIsInstance(dps.resources[0], DataPoint)
        self.assertIsInstance(dps.resources[-1], DataPoint)
        self.assertLessEqual(dps.resources[0].time, start)
        self.assertLessEqual(start, dps.resources[1].time)
        self.assertLessEqual(dps.resources[-2].time, end)
        self.assertLessEqual(end, dps.resources[-1].time)

    def test_list_with_limit(self):
        l = self.client.time_series.list(limit=9)
        self.assertIsInstance(l, TimeSeriesList)
        self.assertEqual(len(l), 9)
        self.assertIsInstance(l.resources[0], TimeSeries)

    def test_retrieve_single_timeseries(self):
        ts = self.client.time_series.retrieve("b51e1723-c25b-4847-825e-2da26409ff3c")
        self.assertIsInstance(ts, TimeSeries)
        self.assertEqual(ts.id, "b51e1723-c25b-4847-825e-2da26409ff3c")

    def test_retrieve_multiple_timeseries(self):
        tsl = self.client.time_series.retrieve_multiple(["bdc2e4aa-83de-458b-b989-675fa4e58aac",
                                                         "b51e1723-c25b-4847-825e-2da26409ff3c"])
        self.assertIsInstance(tsl, TimeSeriesList)
        self.assertEqual(len(tsl), 2)
        self.assertIsInstance(tsl.resources[0], TimeSeries)
        self.assertIsInstance(tsl.resources[1], TimeSeries)
        self.assertEqual(tsl.resources[0].id, "bdc2e4aa-83de-458b-b989-675fa4e58aac")
        self.assertEqual(tsl.resources[1].id, "b51e1723-c25b-4847-825e-2da26409ff3c")

    def test_first_dp(self):
        dp = self.client.time_series.first_data("b51e1723-c25b-4847-825e-2da26409ff3c")
        self.assertIsInstance(dp, DataPoint)
        self.assertIsInstance(dp.time, datetime.datetime)
        self.assertIsInstance(dp.value, (float, int, str))
        self.assertIsInstance(dp.status, int)
        self.assertIsInstance(dp.unit, str)

    def test_latest_dp(self):
        dp = self.client.time_series.latest_data("b51e1723-c25b-4847-825e-2da26409ff3c")
        self.assertIsInstance(dp, DataPoint)
        self.assertIsInstance(dp.time, datetime.datetime)
        self.assertIsInstance(dp.value, (float, int, str))
        self.assertIsInstance(dp.status, int)
        self.assertIsInstance(dp.unit, str)


if __name__ == '__main__':
    unittest.main()
