import unittest
from functions.edfred_site_characteristics_to_common_format.utils import Utils


class UtilsUnitTests(unittest.TestCase):
    def setUp(self):
        self.utils = Utils()

    def test_parse_dms_invalid_value(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("INVALID COORDINATE")

    def test_parse_invalid_direction(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("12° 34' 56.76'' Z'")

    def test_parse_dms_north_latitude_exceeds_max_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("91° 0' 0.0'' N")

    def test_parse_dms_south_latitude_exceeds_max_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("91° 0' 0.0'' S")

    def test_parse_dms_north_latitude_exceeds_min_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("-1° 0' 0.0'' N")

    def test_parse_dms_east_longitude_exceeds_min_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("-1° 0' 0.0'' E")

    def test_parse_dms_west_longitude_exceeds_max_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("181° 0' 0.0'' W")

    def test_parse_dms_east_longitude_exceeds_max_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("181° 0' 0.0'' E")

    def test_parse_dms_west_longitude_exceeds_min_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("-1° 0' 0.0'' W")

    def test_parse_dms_south_latitude_exceeds_min_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("-1° 0' 0.0'' S")

    def test_parse_dms_minutes_exceeds_min_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("12° -1' 0.0'' S")

    def test_parse_dms_minutes_exceeds_max_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("12° 61' 0.0'' S")

    def test_parse_dms_seconds_exceeds_min_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("12° 34' -1.0'' S")

    def test_parse_dms_seconds_exceeds_max_limit(self):
        with self.assertRaises(Exception):
            self.utils.parse_dms("12° 34' 61.0'' S")

    def test_parse_dms_west_longitude(self):
        longitude = "54° 34' 10.12'' W'"
        actual = self.utils.parse_dms(longitude)
        expected = -54.569477777777784
        self.assertEqual(expected, actual, "Failed to parse west longitude")

    def test_parse_dms_east_longitude(self):
        longitude = "34° 56' 23.56'' E'"
        actual = self.utils.parse_dms(longitude)
        expected = 34.939877777777774
        self.assertEqual(expected, actual, "Failed to parse east longitude")

    def test_parse_dms_north_latitude(self):
        latitude = "12° 34' 56.78'' N'"
        actual = self.utils.parse_dms(latitude)
        expected = 12.58243888888889
        self.assertEqual(expected, actual, "Failed to parse north latitude")

    def test_parse_dms_south_latitude(self):
        latitude = "23° 45' 12.34'' S'"
        actual = self.utils.parse_dms(latitude)
        expected = -23.753427777777777
        self.assertEqual(expected, actual, "Failed to parse south latitude")

    def test_parse_dms_no_spaces(self):
        latitude = "23°45'12.34\"S'"
        actual = self.utils.parse_dms(latitude)
        expected = -23.753427777777777
        self.assertEqual(expected, actual, "Failed to parse south latitude")

    def test_striplist(self):
        test_list = ['Trailing ', ' Leading', ' Padded ', 'No Padding']
        actual = self.utils.striplist(test_list)
        expected = ['Trailing', 'Leading', 'Padded', 'No Padding']
        self.assertEqual(expected, actual, "Failed to strip extraneous spaces from list of strings")


if __name__ == '__main__':
    unittest.main()
