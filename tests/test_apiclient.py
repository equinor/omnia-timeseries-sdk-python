import unittest
import datetime
from omnia_timeseries_sdk import OmniaClient
from omnia_timeseries_sdk.resources import TimeSeries, TimeSeriesList, DataPoint, DataPoints
from omnia_timeseries_sdk.exceptions import OmniaTimeSeriesAPIError


class CreateAndDeleteDataPointsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = OmniaClient()
        self.name = "PYSDK_TEST_SERIES"
        self.description = "Time series instance created for testing API."
        self.unit = "horse"
        self.asset_id = None
        self.external_id = None
        self.step = False
        self.ts = self.client.time_series.create(self.name, description=self.description, unit=self.unit,
                                                 asset_id=self.asset_id, external_id=self.external_id, step=self.step)
        self.t0 = datetime.datetime(2020, 1, 1, hour=12, minute=0, second=0)
        self.dt = datetime.timedelta(days=1)
        self.ts.add_data([self.t0, self.t0 + self.dt], [100, 200], [0, 0])

    def test_instance(self):
        dps = self.ts.data()
        self.assertIsInstance(dps, DataPoints)
        self.assertEqual(2, len(dps))
        self.assertEqual(self.ts.id, dps.id)
        self.assertEqual([100, 200], dps.value)
        self.assertEqual([0, 0], dps.status)

        dps = self.ts.data(start_time=(self.t0 + self.dt / 2))
        self.assertIsInstance(dps, DataPoints)
        self.assertEqual(1, len(dps))
        self.assertEqual(self.ts.id, dps.id)
        self.assertEqual([200], dps.value)
        self.assertEqual([0], dps.status)

    def tearDown(self) -> None:
        try:
            _ = self.ts.delete_data()
        except OmniaTimeSeriesAPIError as e:
            raise e
        else:
            dps = self.ts.data()
            if not len(dps) == 0:
                self.fail(f"The data points on time series '{self.ts.id}' still exist.")
        finally:
            _ = self.ts.delete()
            try:
                _ = self.client.time_series.retrieve(self.ts.id)
            except OmniaTimeSeriesAPIError as e:
                self.assertEqual(404, int(e.status))
            else:
                self.fail(f"Time series '{self.ts.id}' still exists.")


class CreateAndDeleteTimeSeriesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = OmniaClient()
        self.name = "PYSDK_TEST_SERIES"
        self.description = "Time series instance created for testing API."
        self.unit = "horse"
        self.asset_id = None
        self.external_id = None
        self.step = False
        self.ts = self.client.time_series.create(self.name, description=self.description, unit=self.unit,
                                                 asset_id=self.asset_id, external_id=self.external_id, step=self.step)

    def test_instance(self):
        self.assertIsInstance(self.ts, TimeSeries)
        self.assertEqual(self.name, self.ts.name)
        self.assertEqual(self.description, self.ts.description)
        self.assertEqual(self.unit, self.ts.unit)
        self.assertIsNone(self.ts.asset_id)
        self.assertIsNone(self.ts.external_id)
        self.assertFalse(self.ts.step)

        # is it retrievable
        _ = self.client.time_series.retrieve(self.ts.id)
        self.assertIsInstance(_, TimeSeries)
        self.assertEqual(self.ts.id, _.id)
        self.assertEqual(self.ts.name, _.name)

    def tearDown(self) -> None:
        r = self.ts.delete()
        try:
            _ = self.client.time_series.retrieve(self.ts.id)
        except OmniaTimeSeriesAPIError as e:
            self.assertEqual(404, int(e.status))
        else:
            self.fail(f"Time series '{self.ts.id}' is still retrievable.")


class RetrieveExistingTimeSeriesAndDataPointsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = OmniaClient()

    def tearDown(self) -> None:
        pass

    def test_data_with_limit(self):
        end = datetime.datetime(2019, 11, 20, hour=12, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
        start = end - datetime.timedelta(hours=1)
        dps = self.client.time_series.data("b51e1723-c25b-4847-825e-2da26409ff3c", limit=10, start_time=start.isoformat(),
                                           end_time=end.isoformat())
        self.assertIsInstance(dps, DataPoints)
        self.assertEqual(len(dps), 10)
        self.assertIsInstance(dps.resources[0], DataPoint)

    def test_data(self):
        dps = self.client.time_series.data("b51e1723-c25b-4847-825e-2da26409ff3c")
        self.assertIsInstance(dps, DataPoints)
        self.assertIsInstance(dps.resources[0], DataPoint)
        self.assertIsInstance(dps.resources[-1], DataPoint)
        self.assertLessEqual(dps.resources[-1].time - dps.resources[0].time, datetime.timedelta(days=1))

    def test_data_with_twin(self):
        end = datetime.datetime(2019, 11, 20, hour=12, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
        start = end - datetime.timedelta(hours=1)
        dps = self.client.time_series.data("b51e1723-c25b-4847-825e-2da26409ff3c", start_time=start.isoformat(),
                                           end_time=end.isoformat())
        self.assertIsInstance(dps, DataPoints)
        self.assertIsInstance(dps.resources[0], DataPoint)
        self.assertIsInstance(dps.resources[-1], DataPoint)
        self.assertLessEqual(start, dps.resources[0].time)
        self.assertLessEqual(dps.resources[-1].time, end)

    def test_data_with_twin_including_outside_points(self):
        end = datetime.datetime(2019, 11, 20, hour=12, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
        start = end - datetime.timedelta(hours=1)
        dps = self.client.time_series.data("b51e1723-c25b-4847-825e-2da26409ff3c", start_time=start.isoformat(),
                                           end_time=end.isoformat(), include_outside_points=True)
        self.assertIsInstance(dps, DataPoints)
        self.assertIsInstance(dps.resources[0], DataPoint)
        self.assertIsInstance(dps.resources[-1], DataPoint)
        self.assertLessEqual(dps.resources[0].time, start)
        self.assertLessEqual(start, dps.resources[1].time)
        self.assertLessEqual(dps.resources[-2].time, end)
        self.assertLessEqual(end, dps.resources[-1].time)

    def test_list(self):
        l = self.client.time_series.list(limit=9)
        self.assertIsInstance(l, TimeSeriesList)

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
