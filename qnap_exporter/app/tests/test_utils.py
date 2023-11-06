import unittest
from qnap_exporter.app import utils


class TestUtils(unittest.TestCase):
    def test_garmin_id_from_strava(self):
        prefix = 'garmin_push_'
        strava_external_id = 'garmin_push_12345'
        garmin_id = '12345'
        self.assertIn(prefix, strava_external_id)
        self.assertIn(garmin_id, strava_external_id)
        found_id = utils.garmin_activity_from_strava(strava_external_id)
        self.assertIsNotNone(found_id)
        self.assertIsInstance(found_id, str)
        self.assertEqual(found_id, garmin_id)
        reconstruct = f'{prefix}{found_id}'
        self.assertEqual(strava_external_id, reconstruct)


if __name__ == '__main__':
    unittest.main()
