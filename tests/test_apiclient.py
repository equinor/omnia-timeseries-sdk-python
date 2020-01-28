import os
import unittest
import datetime
from omnia_timeseries_sdk import OmniaClient
from omnia_timeseries_sdk._config import TestConfig
from omnia_timeseries_sdk.resources import TimeSeries, TimeSeriesList, DataPoint, DataPoints
from omnia_timeseries_sdk.exceptions import OmniaTimeSeriesAPIError


@unittest.skipIf(
    os.getenv("omniaClientSecret") is None,
    reason="Skipping test. The shared client secret 'omniaClientSecret' is not set in environment variable")
class TimeseriesDatapointsIntegrationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = OmniaClient(config=TestConfig)

        # avoid potential conflicts (remove remains from unsuccessful tests).
        for ts in self.client.time_series.list(name="PYSDK_TEST_SERIES"):
            try:
                ts.delete_data()
            except OmniaTimeSeriesAPIError:
                pass

            try:
                ts.delete()
            except OmniaTimeSeriesAPIError:
                pass

        # create time series and datapoints
        self.ts1 = self.client.time_series.create(
            "PYSDK_TEST_SERIES",
            description="Time series instance created for testing API.",
            unit="horse",
            asset_id=None, external_id=None, step=False
        )
        self.ts2 = self.client.time_series.create(
            "PYSDK_TEST_SERIES_TWO",
            description="Time series instance created for testing API.",
            unit="horse",
            asset_id=None, external_id=None, step=False
        )
        self.t0 = datetime.datetime(2020, 1, 1, hour=12, minute=0, second=0, tzinfo=datetime.timezone.utc)
        self.dt = datetime.timedelta(days=1)
        self.ts1.add_data([self.t0, self.t0 + self.dt, self.t0 + 2 * self.dt], [100, 200, 150], [0, 0, 0])

    def test_create(self):
        self.assertIsInstance(self.ts1, TimeSeries)
        self.assertEqual("PYSDK_TEST_SERIES", self.ts1.name)
        self.assertEqual("Time series instance created for testing API.", self.ts1.description)
        self.assertEqual("horse", self.ts1.unit)
        self.assertIsNone(self.ts1.asset_id)
        self.assertIsNone(self.ts1.external_id)
        self.assertFalse(self.ts1.step)

    def test_retrieve(self):
        _ = self.client.time_series.retrieve(self.ts1.id)
        self.assertIsInstance(_, TimeSeries)
        self.assertEqual(self.ts1.id, _.id)
        self.assertEqual(self.ts1.name, _.name)

    def test_retrieve_multiple(self):
        _ = self.client.time_series.retrieve_multiple([self.ts1.id, self.ts2.id])
        self.assertIsInstance(_, TimeSeriesList)
        self.assertEqual(2, len(_))
        self.assertIsInstance(_.resources[0], TimeSeries)
        self.assertIsInstance(_.resources[1], TimeSeries)
        self.assertEqual(_.resources[0].id, self.ts1.id)
        self.assertEqual(_.resources[1].id, self.ts2.id)

    def test_list(self):
        _ = self.client.time_series.list()
        self.assertIsInstance(_, TimeSeriesList)

    def test_update(self):
        self.ts1.update(unit="donkey")
        self.assertIsInstance(self.ts1, TimeSeries)
        self.assertEqual("PYSDK_TEST_SERIES", self.ts1.name)
        self.assertEqual("Time series instance created for testing API.", self.ts1.description)
        self.assertEqual("donkey", self.ts1.unit)
        self.assertIsNone(self.ts1.asset_id)
        self.assertIsNone(self.ts1.external_id)
        self.assertFalse(self.ts1.step)

    def test_first_dp(self):
        dp = self.ts1.first()
        self.assertIsInstance(dp, DataPoint)
        self.assertIsInstance(dp.time, datetime.datetime)
        self.assertIsInstance(dp.value, (int, float))
        self.assertIsInstance(dp.status, int)
        self.assertIsInstance(dp.unit, str)
        self.assertEqual(100, dp.value)
        self.assertEqual(datetime.datetime(2020, 1, 1, hour=12, minute=0, second=0, tzinfo=datetime.timezone.utc), dp.time)

    def test_latest_dp(self):
        dp = self.ts1.latest()
        self.assertIsInstance(dp, DataPoint)
        self.assertIsInstance(dp.time, datetime.datetime)
        self.assertIsInstance(dp.value, (int, float))
        self.assertIsInstance(dp.status, int)
        self.assertIsInstance(dp.unit, str)
        self.assertEqual(150, dp.value)
        self.assertEqual(datetime.datetime(2020, 1, 3, hour=12, minute=0, second=0, tzinfo=datetime.timezone.utc), dp.time)

    def test_dps_in_twin(self):
        start = self.t0 - datetime.timedelta(days=1)
        end = self.t0 + datetime.timedelta(days=1.5)
        dps = self.ts1.data(start_time=start.isoformat(),
                            end_time=end.isoformat())
        self.assertIsInstance(dps, DataPoints)
        self.assertEqual(2, len(dps))
        self.assertEqual(self.ts1.id, dps.id)
        self.assertEqual([100, 200], dps.value)
        self.assertIsInstance(dps.resources[0], DataPoint)
        self.assertIsInstance(dps.resources[1], DataPoint)
        for dp in dps:
            self.assertGreaterEqual(dp.time, start)
            self.assertLessEqual(dp.time, end)

    def test_dps_after_time(self):
        start = self.t0 + datetime.timedelta(hours=12)
        dps = self.ts1.data(start_time=start.isoformat())
        self.assertIsInstance(dps, DataPoints)
        self.assertEqual(2, len(dps))
        self.assertEqual(self.ts1.id, dps.id)
        self.assertEqual([200, 150], dps.value)
        for dp in dps:
            self.assertGreaterEqual(dp.time, start)

    def test_include_outside_dps(self):
        start = self.t0 + datetime.timedelta(hours=12)
        dps = self.ts1.data(start_time=start.isoformat(), include_outside_points=True)
        self.assertIsInstance(dps, DataPoints)
        self.assertEqual(3, len(dps))
        self.assertEqual(self.ts1.id, dps.id)
        self.assertEqual([100, 200, 150], dps.value)

    def tearDown(self) -> None:
        for ts in [self.ts1, self.ts2]:
            # delete data points
            try:
                _ = ts.delete_data()
            except OmniaTimeSeriesAPIError as e:
                # NB: Timeseries API v1.5 has a bug that raises an internal server error (code 500) even though the
                #  datapoints are deleted.
                # TODO: Reformulate once the timeseries API bug is corrected
                pass

            # check that the data points were actually deleted
            dps = ts.data()
            if not len(dps) == 0:
                self.fail(f"The data points on time series '{ts.id}' still exist.")

            # delete time series
            _ = ts.delete()
            try:
                _ = self.client.time_series.retrieve(ts.id)
            except OmniaTimeSeriesAPIError as e:
                self.assertEqual(404, int(e.status))
            else:
                self.fail(f"Time series '{ts.id}' still exists.")


if __name__ == '__main__':
    unittest.main()
