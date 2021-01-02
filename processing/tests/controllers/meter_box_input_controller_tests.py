import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from processing.data_objects import MeterBoxDO
from processing.meter_box_input_controller import MeterBoxInputController

METERBOX_INPUT_DATA = {
    'MeterReference': ['PROJ_ECP001_S3_METER001'],
    'Deeper level asset reference': ['PROJ_ECP001_S3_SUB001LevHv01Upgrid01Cell'],
    'MeterKind': ['METERKIND'],
    'Layer_ALL_Contractual': ['PROJ'],
    'Layer_ALL_ISOGeographical': ['COUNTRY'],
    'Naming_InverterStation_Contractual': ['NULL']
}


class MeterBoxInputControllerTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.met_station_dos = []
        self.controller = MeterBoxInputController(project_code='PROJ', country='COUNTRY')
        self.meter_box_dos = [
            MeterBoxDO(
                name=None,
                iec_name='PROJ_ECP001_S3_METER001',
                deeper_level_asset_ref='PROJ_ECP001_S3_SUB001LevHv01Upgrid01Cell',
                meterkind='METERKIND')
        ]

    def test_get_meter_input_dataframe(self):
        expected = pd.DataFrame(METERBOX_INPUT_DATA)
        actual = self.controller.get_meter_box_dataframe(meter_box_dos=self.meter_box_dos)
        assert_frame_equal(expected, actual)


if __name__ == '__main__':
    unittest.main()
