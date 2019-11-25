import unittest
import datetime
from omnia_timeseries_sdk._utils import from_datetime_string, to_omnia_datetime_string, to_camel_case, to_snake_case


class UtilsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data = dict(assetId="hldhaf645",
                         name="something",
                         externalId="ad646d7fad1fa6d84f6",
                         data=[
                             dict(subAssetId="ad684fa", created=datetime.datetime.utcnow()),
                             dict(subAssetId="qw77wtg", created=datetime.datetime.utcnow()),
                         ])

    def test_snake_dict(self):
        d = to_snake_case(self.data)
        d2 = d.get("data")[0]   # need only one
        self.assertIn("asset_id", d)
        self.assertIn("external_id", d)
        self.assertIn("name", d)
        self.assertIn("data", d)
        self.assertIn("sub_asset_id", d2)
        self.assertIn("created", d2)

    def test_snake_str(self):
        s = to_snake_case("someCamelCasedString")
        self.assertEqual(s, "some_camel_cased_string")

    def test_camel_dict(self):
        d = to_camel_case(to_snake_case(self.data))
        d2 = d.get("data")[0]   # need only one
        self.assertIn("assetId", d)
        self.assertIn("externalId", d)
        self.assertIn("name", d)
        self.assertIn("data", d)
        self.assertIn("subAssetId", d2)
        self.assertIn("created", d2)

    def test_datetime_strings(self):
        s = "2008-09-03T20:56:35.450686Z"
        self.assertEqual(s, to_omnia_datetime_string(from_datetime_string("2008-09-03T20:56:35.450686Z")))
        self.assertEqual(s, to_omnia_datetime_string(from_datetime_string("2008-09-03T20:56:35.450686+00:00")))


if __name__ == '__main__':
    unittest.main()
