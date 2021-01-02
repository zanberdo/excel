import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from processing.data_objects import MetStationDO
from processing.met_station_input_controller import MetStationInputController

MET_STATION_INPUT_DATA = {
    'SQL extract': ['PROJ-TT00-Pad', 'PROJ-TT01-Pad'],
    'MetSta number': ['00', '01'],
    'LDevice_inst': ['PROJ_ECP001_S3_METEOSTA000', 'PROJ_ECP001_S3_METEOSTA001'],
    'Layer_ALL_Contractual': ['PROJ', 'PROJ'],
    'Layer_ALL_ISOGeographical': ['COUNTRY', 'COUNTRY'],
    'Naming_EnvironmentalMonitoringStation_Contractual': ['PROJ-TT00-Pad', 'PROJ-TT01-Pad'],
    'POASensor_number': [1, 1],
    'GHISensor_number': [4, 4],
    'BackOfModuleTempSensor_number': [5, 5],
    'AmbientTempSensor_number': [6, 6]}


class MetStationInputControllerTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.met_station_dos = []
        self.controller = MetStationInputController(project_code='PROJ', country='COUNTRY')
        for i in range(2):
            self.met_station_dos.append(
                MetStationDO(
                    name=f'TT0{i}-Pad',
                    iec_name=f'PROJ_ECP001_S3_METEOSTA00{i}',
                    number_of_poa_sensors=1,
                    iec_pos_sensors='POAinSOL[1]',
                    number_of_rear_facing_sensors=2,
                    number_of_irradiance_sensors=3,
                    number_of_ghi_sensors=4,
                    number_of_bom_temp_sensors=5,
                    iec_bom_temperature_sensors='PVSTMP[1]',
                    number_of_ambient_temp_sensors=6)
            )

    def test_get_met_station_input_dataframe(self):
        expected = pd.DataFrame(MET_STATION_INPUT_DATA)
        actual = self.controller.get_met_station_dataframe(met_station_dos=self.met_station_dos)
        assert_frame_equal(expected, actual)


if __name__ == '__main__':
    unittest.main()
