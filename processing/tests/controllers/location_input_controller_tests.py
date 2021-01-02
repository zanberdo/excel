import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

import pandas as pd
from pandas.testing import assert_frame_equal

from processing.data_objects import SiteLevelDO
from processing.location_input_controller import LocationInputController

LOCATION_INPUT_DATA = {
    'Location-type': ['ContractualInfo'],
    'Location-Name': ['ContractualProjectPROJ'],
    'Location-description': [
        'Location defining the coordinate system for PROJ, based on average inverter location'],
    'crsUrn_CS': ['urn:ogc:dev:crs:EPSG::4326'],
    'xPosition': ['LONGITUDE'],
    'yPosition': ['LATITUDE'],
    'zPosition': ['NULL'],
    'Layer-Name': ['PROJ'],
    'name_StreetAddress': ['NULL'],
    'projectCode': ['NULL'],
    'geoInfoReference': ['NULL']
}


class LocationInputControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    @patch('src.functions.lambdas.edfred_solar_site_onboarding_to_common_format.location_input_controller.Utils')
    @patch('src.functions.lambdas.edfred_solar_site_onboarding_to_common_format.data_objects.Utils')
    def test_get_location_input_dataframe(self, mock_controller_utils, mock_do_utils):
        mock_controller_magic_mock = MagicMock()
        mock_controller_magic_mock.get_country_by_lat_long.return_value = "COUNTRY"
        mock_controller_utils.return_value = mock_controller_magic_mock

        mock_do_utils().parse_dms.side_effect = ["LONGITUDE", "LATITUDE"]
        controller = LocationInputController()

        expected = pd.DataFrame(LOCATION_INPUT_DATA)
        self.site_level_dos = [
            SiteLevelDO(
                project_code='PROJ',
                iec_name='IEC NAME',
                latitude='LATITUDE',
                longitude='LONGITUDE',
                module_tilt='MODULE TILT',
                module_orientation='MODULE ORIENTATION',
                capacity_limit_wac=11_111_111,
                total_capacity_wdc=22_222_222,
                number_of_feeders=3,
                cod=datetime(2020, 12, 1)
            )]
        actual = controller.get_location_dataframe(site_level_dos=self.site_level_dos)
        assert_frame_equal(expected, actual)


if __name__ == '__main__':
    unittest.main()
