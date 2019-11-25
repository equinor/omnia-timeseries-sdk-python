import unittest
import omnia_timeseries_sdk


class GeneralTestCase(unittest.TestCase):
    def test_version(self):
        self.assertIsInstance(omnia_timeseries_sdk.__version__, str)


if __name__ == '__main__':
    unittest.main()
