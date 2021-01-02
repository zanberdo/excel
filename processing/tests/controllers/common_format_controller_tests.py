import logging
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from processing.common_format_controller import CommonFormatController

MSG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(format=MSG_FORMAT, datefmt=DATETIME_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@unittest.skip('Skipping all unit tests until tests fleshed out')
class CommonFormatControllerTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.patcher = patch('src.functions.lambdas.edfred_solar_site_onboarding_to_common_format.data_objects.'
                             'site_level_do.Utils')
        self.mock_site_level_do_utils = self.patcher.start()
        self.mock_site_level_do_magic_mock = MagicMock()
        self.mock_site_level_do_magic_mock.get_country_by_lat_long.return_value = 'COUNTRY'
        self.mock_site_level_do_utils.return_value = self.mock_site_level_do_magic_mock

        with mock.patch('s3fs.S3FileSystem') as mock_fs:
            self.controller = CommonFormatController('PROJECT CODE', mock_fs)

    def tearDown(self) -> None:
        self.patcher.stop()

    def test_write_met_station_input(self):
        # TODO: mock location input controller - repeat as needed for the remaining test
        #       mock dataframe returned by get_input_dataframe(ANY, ...)
        #       verify call to get_input_dataframe
        #       verify call to __write_common_file(ANY, ANY)
        self.assertEqual(True, False)

    def test_write_location_input(self):
        self.assertEqual(True, False)

    def test_write_electrical_input(self):
        self.assertEqual(True, False)

    def test_write_meter_box_input(self):
        self.assertEqual(True, False)

    def test_write_meas_input(self):
        self.assertEqual(True, False)

    def test_write_asset_list_input(self):
        self.assertEqual(True, False)

    def test_write_asset_info_input(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
