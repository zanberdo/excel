import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

import pandas as pd

from processing.data_objects import CombinerDO
from processing.data_objects import FeederDO
from processing.data_objects import InverterDO
from processing.data_objects import MetStationDO
from processing.data_objects import MeterBoxDO
from processing.data_objects import SensorDO
from processing.data_objects import ShelterDO
from processing.data_objects import SiteLevelDO
from processing.data_objects import SiteLevelNonElecDO
from processing.data_objects import SoilingStationDO
from processing.data_objects import TrackerDO
from processing.site_characteristics_controller import SiteCharacteristicsController

SITE_LEVEL_DATA = {
    0: [None, None, None, None, None, None, None, None, None, None],
    1: ['Placeholder01', 'Placeholder02', 'Placeholder03', 'Placeholder04', 'Placeholder05', 'Placeholder06',
        'Placeholder07', 'Placeholder08', 'Placeholder09', 'Placeholder10'],
    2: [None, None, None, None, None, None, None, None, None, None],
    3: ['PROJECT CODE', 'IEC NAME', 'LATITUDE', 'LONGITUDE', 'MODULE TILT', 'MODULE ORIENTATION', 11_111_111,
        22_222_222, 3, datetime(2020, 12, 1)]
}

FEEDER_DATA = {
    0: [None, None, None, None, None, None, None],
    1: ['Placeholder01', 'Placeholder02', 'Placeholder03', 'Placeholder04', 'Placeholder05', 'Placeholder06',
        'Placeholder07'],
    2: [None, None, None, None, None, None, None],
    3: ['FEEDER NAME 01', 'IEC NAME 01', 1_111_111, 2_222_222, 3, datetime(2020, 12, 1), 'CONTRACT PROJECT CODE 01'],
    4: ['FEEDER NAME 02', 'IEC NAME 02', 4_444_444, 5_555_555, 6, datetime(2020, 12, 1), 'CONTRACT PROJECT CODE 02'],
    5: [None, None, None, None, None, None, None],
    6: [None, None, None, None, None, None, None],
    7: [None, None, None, None, None, None, None],
    8: [None, None, None, None, None, None, None],
    9: [None, None, None, None, None, None, None],
    10: [None, None, None, None, None, None, None]
}

SHELTER_DATA = {
    0: [None, None, None, None, None, None],
    1: ['Placeholder01', 'Placeholder02', 'Placeholder03', 'Placeholder04', 'Placeholder05', 'Placeholder06'],
    2: [None, None, None, None, None, None],
    3: ['SHELTER NAME 01', 'IEC NAME 01', 11_111_111, 22_222_222, 3, 'PARENT FEEDER 01'],
    4: ['SHELTER NAME 02', 'IEC NAME 02', 44_444_444, 55_555_555, 6, 'PARENT FEEDER 02'],
    5: ['SHELTER NAME 03', 'IEC NAME 03', 77_777_777, 88_888_888, 9, 'PARENT FEEDER 03'],
    6: [None, None, None, None, None, None]
}

INVERTER_DATA = {
    0: [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None],
    1: ['Placeholder01', 'Placeholder02', 'Placeholder03', 'Placeholder04', 'Placeholder05', 'Placeholder06',
        'Placeholder07', 'Placeholder08', 'Placeholder09', 'Placeholder10', 'Placeholder11', 'Placeholder12',
        'Placeholder13', 'Placeholder14', 'Placeholder15', 'Placeholder16', 'Placeholder17', 'Placeholder18',
        'Placeholder19', 'Placeholder20'],
    2: [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None],
    3: ['INVERTER NAME 01', 'IEC NAME 01', 111_111, None, 222_222, None, 'MANUFACTURER 01', 'MODEL 01',
        'EVENTLIST NAME 01', 100, 200, 1_000, 2_000, 100_000, 200_000, 300_000, None, None, 99, 'F'],
    4: ['INVERTER NAME 02', 'IEC NAME 02', 333_333, None, 444_444, None, 'MANUFACTURER 02', 'MODEL 02',
        'EVENTLIST NAME 02', 100, 200, 1_000, 2_000, 100_000, 200_000, 300_000, None, None, 99, 'F'],
    5: ['INVERTER NAME 03', 'IEC NAME 03', 555_555, None, 666_666, None, 'MANUFACTURER 03', 'MODEL 03',
        'EVENTLIST NAME 03', 100, 200, 1_000, 2_000, 100_000, 200_000, 300_000, None, None, 99, 'F'],
    6: [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None]
}

COMBINER_DATA = {
    0: [None, None, None, None, None, None, None, None, None],
    1: ['Placeholder01', 'Placeholder02', 'Placeholder03', 'Placeholder04', 'Placeholder05', 'Placeholder06',
        'Placeholder07', 'Placeholder08', 'Placeholder09'],
    2: [None, None, None, None, None, None, None, None, None],
    3: ['COMBINER NAME 01', 'IEC NAME 01', 11_111, 'MANUFACTURER 01', 'MODEL 01', -0.0123, 0.0123, 0.0456, None],
    4: ['COMBINER NAME 02', 'IEC NAME 02', 22_222, 'MANUFACTURER 02', 'MODEL 02', -0.0456, 0.0456, 0.0789, None],
    5: ['COMBINER NAME 03', 'IEC NAME 03', 33_333, 'MANUFACTURER 03', 'MODEL 03', -0.9876, 0.5432, 0.0100, None],
    6: [None, None, None, None, None, None, None, None, None]
}

SITE_LEVEL_NON_ELEC_DATA = {
    0: [None, None],
    1: ['Placeholder01', 'Placeholder02'],
    2: [None, None],
    3: [1, 2],
    4: [None, None]
}

MET_STATION_DATA = {
    0: [None, None, None, None, None, None, None, None, None, None],
    1: ['Placeholder01', 'Placeholder02', 'Placeholder03', 'Placeholder04', 'Placeholder05',
        'Placeholder06', 'Placeholder07', 'Placeholder08', 'Placeholder09', 'Placeholder10'],
    2: [None, None, None, None, None, None, None, None, None, None],
    3: ['MET STATION NAME 01', 'IEC NAME 01', 1, 'IEC POA SENSORS 01', 2, 3, 4, 5, 'IEC BOM TEMPERATURE 01', 6],
    4: ['MET STATION NAME 02', 'IEC NAME 02', 2, 'IEC POA SENSORS 02', 2, 3, 4, 5, 'IEC BOM TEMPERATURE 02', 6],
    5: ['MET STATION NAME 03', 'IEC NAME 03', 3, 'IEC POA SENSORS 03', 2, 3, 4, 5, 'IEC BOM TEMPERATURE 03', 6],
    6: [None, None, None, None, None, None, None, None, None, None]
}

SENSOR_DATA = {
    0: [None, None, None, None, None, None, None],
    1: ['Placeholder01', 'Placeholder02', 'Placeholder03', 'Placeholder04', 'Placeholder05', 'Placeholder06',
        'Placeholder07'],
    2: [None, None, None, None, None, None, None],
    3: ['SENSOR NAME 01', None, 'MANUFACTURER 01', 'MODEL 01', None, None, 'SENSOR TYPE 01'],
    4: ['SENSOR NAME 02', None, 'MANUFACTURER 02', 'MODEL 02', None, None, 'SENSOR TYPE 02'],
    5: ['SENSOR NAME 03', None, 'MANUFACTURER 03', 'MODEL 03', None, None, 'SENSOR TYPE 03'],
    6: [None, None, None, None, None, None, None]
}

SOILING_STATION_DATA = {
    0: [None, None, None, None],
    1: ['Placeholder01', 'Placeholder02', 'Placeholder03', 'Placeholder04'],
    2: [None, None, None, None],
    3: ['SOILING STATION NAME', 0.012, 12345, 56789],
    4: [None, None, None, None]
}

TRACKER_DATA = {
    0: [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None],
    1: ['Placeholder01', 'Placeholder02', 'Placeholder03', 'Placeholder04', 'Placeholder05', 'Placeholder06',
        'Placeholder07', 'Placeholder08', 'Placeholder09', 'Placeholder10', 'Placeholder11', 'Placeholder12',
        'Placeholder13', 'Placeholder14', 'Placeholder15', 'Placeholder16', 'Placeholder17', 'Placeholder18',
        'Placeholder19'
        ],
    2: [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None],
    3: ['TRACKER NAME 01', 'MANUFACTURER 01', 'MODEL 01', 1, 1, 1, 'CONTROL ALGORITHM 01', 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1],
    4: ['TRACKER NAME 02', 'MANUFACTURER 02', 'MODEL 02', 2, 2, 2, 'CONTROL ALGORITHM 02', 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2],
    5: ['TRACKER NAME 03', 'MANUFACTURER 03', 'MODEL 03', 3, 3, 3, 'CONTROL ALGORITHM 03', 3, 3, 3, 3, 3, 3, 3, 3, 3,
        3, 3, 3],
    6: [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        None]
}

METER_BOX_DATA = {
    0: [None, None, None, None],
    1: ['Placeholder01', 'Placeholder02', 'Placeholder03', 'Placeholder04'],
    2: [None, None, None, None],
    3: ['METER BOX NAME', 'IEC NAME', 'DEEPER LEVEL ASSET', 'METERKIND'],
    4: [None, None, None, None]
}

DATA_COLUMN_OFFSET = 3


class SiteCharacteristicsControllerTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.patcher = patch(
            'src.functions.lambdas.edfred_solar_site_onboarding_to_common_format.site_characteristics_controller.Utils')
        self.mock_controller_utils = self.patcher.start()
        self.mock_controller_magic_mock = MagicMock()
        self.mock_controller_magic_mock.is_column_empty.return_value = False
        self.mock_controller_utils.return_value = self.mock_controller_magic_mock
        self.controller = SiteCharacteristicsController(DATA_COLUMN_OFFSET)

    def tearDown(self) -> None:
        self.patcher.stop()

    def test_get_site_level_throws_exception(self):
        with self.assertRaises(Exception):
            self.controller.get_site_level(dataframe='dataframe', row_offset=0, rows=1)

    @patch('src.functions.lambdas.edfred_solar_site_onboarding_to_common_format.data_objects.Utils')
    def test_get_site_level(self, mock_do_utils):
        mock_do_magic_mock = MagicMock()
        mock_do_magic_mock.get_country_by_lat_long.return_value = "COUNTRY"
        mock_do_utils.return_value = mock_do_magic_mock

        dataframe = pd.DataFrame(SITE_LEVEL_DATA)
        expected = [
            SiteLevelDO(project_code='PROJECT CODE',
                        iec_name='IEC NAME',
                        latitude='LATITUDE',
                        longitude='LONGITUDE',
                        module_tilt='MODULE TILT',
                        module_orientation='MODULE ORIENTATION',
                        capacity_limit_wac=11111111,
                        total_capacity_wdc=22222222,
                        number_of_feeders=3,
                        cod=datetime(2020, 12, 1))
        ]
        actual = self.controller.get_site_level(dataframe=dataframe, row_offset=0, rows=10)
        self.assertListEqual(expected, actual, 'Failed to assert expected SiteLevelDO')

    @patch('src.functions.lambdas.edfred_solar_site_onboarding_to_common_format.data_objects.Utils')
    @patch('src.functions.lambdas.edfred_solar_site_onboarding_to_common_format.site_characteristics_controller.Utils')
    def test_get_site_level_data_column_offset_2(self, mock_do_utils, mock_controller_utils):
        DATA_COLUMN_OFFSET_2 = 2
        SITE_LEVEL_DATA_COLUMN_OFFSET_2 = {
            0: [None, None, None, None, None, None, None, None, None, None],
            1: ['Placeholder01', 'Placeholder02', 'Placeholder03', 'Placeholder04', 'Placeholder05', 'Placeholder06',
                'Placeholder07', 'Placeholder08', 'Placeholder09', 'Placeholder10'],
            2: ['PROJECT CODE', 'IEC NAME', 'LATITUDE', 'LONGITUDE', 'MODULE TILT', 'MODULE ORIENTATION', 11_111_111,
                22_222_222, 3, datetime(2020, 12, 1)]
        }

        mock_do_magic_mock = MagicMock()
        mock_do_magic_mock.get_country_by_lat_long.return_value = "COUNTRY"
        mock_do_utils.return_value = mock_do_magic_mock

        mock_controller_utils.is_column_empty.return_value = False
        controller = SiteCharacteristicsController(DATA_COLUMN_OFFSET_2)

        dataframe = pd.DataFrame(SITE_LEVEL_DATA_COLUMN_OFFSET_2)
        expected = [
            SiteLevelDO(project_code='PROJECT CODE',
                        iec_name='IEC NAME',
                        latitude='LATITUDE',
                        longitude='LONGITUDE',
                        module_tilt='MODULE TILT',
                        module_orientation='MODULE ORIENTATION',
                        capacity_limit_wac=11111111,
                        total_capacity_wdc=22222222,
                        number_of_feeders=3,
                        cod=datetime(2020, 12, 1))
        ]
        actual = controller.get_site_level(dataframe=dataframe, row_offset=0, rows=10)
        self.assertListEqual(expected, actual, 'Failed to assert expected SiteLevelDO')

    def test_get_feeders(self):
        dataframe = pd.DataFrame(FEEDER_DATA)
        expected = [
            FeederDO(name='FEEDER NAME 01',
                     iec_name='IEC NAME 01',
                     capacity_wac=1_111_111,
                     capacity_wdc=2_222_222,
                     number_of_shelters_inverters=3,
                     cod=datetime(2020, 12, 1),
                     contract_project_code='CONTRACT PROJECT CODE 01'),
            FeederDO(name='FEEDER NAME 02',
                     iec_name='IEC NAME 02',
                     capacity_wac=4_444_444,
                     capacity_wdc=5_555_555,
                     number_of_shelters_inverters=6,
                     cod=datetime(2020, 12, 1),
                     contract_project_code='CONTRACT PROJECT CODE 02')
        ]
        actual = self.controller.get_feeders(dataframe=dataframe, row_offset=0, rows=7)
        self.assertListEqual(expected, actual, 'Failed to assert expected FeederDO')

    def test_get_shelters(self):
        dataframe = pd.DataFrame(SHELTER_DATA)
        expected = [
            ShelterDO(name='SHELTER NAME 01',
                      iec_name='IEC NAME 01',
                      capacity_wac=11_111_111,
                      capacity_wdc=22_222_222,
                      number_of_inverters_per_shelter=3,
                      parent_feeder='PARENT FEEDER 01'),
            ShelterDO(name='SHELTER NAME 02',
                      iec_name='IEC NAME 02',
                      capacity_wac=44_444_444,
                      capacity_wdc=55_555_555,
                      number_of_inverters_per_shelter=6,
                      parent_feeder='PARENT FEEDER 02'),
            ShelterDO(name='SHELTER NAME 03',
                      iec_name='IEC NAME 03',
                      capacity_wac=77_777_777,
                      capacity_wdc=88_888_888,
                      number_of_inverters_per_shelter=9,
                      parent_feeder='PARENT FEEDER 03')
        ]
        actual = self.controller.get_shelters(dataframe=dataframe, row_offset=0, rows=6)
        self.assertListEqual(expected, actual, 'Failed to assert expected ShelterDO')

    def test_get_inverters(self):
        dataframe = pd.DataFrame(INVERTER_DATA)
        expected = [
            InverterDO(name='INVERTER NAME 01',
                       iec_name='IEC NAME 01',
                       nominal_power_wac=11_1111,
                       maximum_power_kwac=None,
                       total_dc_power=222_222,
                       states_and_fault_codes=None,
                       manufacturer='MANUFACTURER 01',
                       model='MODEL 01',
                       eventlist_name='EVENTLIST NAME 01',
                       umpp_min=100,
                       umpp_max=200,
                       dc_max_voltage=1_000,
                       dc_max_current=2_000,
                       dc_max_power=100_000,
                       dc_nameplate=200_000,
                       dc_peak_power=300_000,
                       firmware_version=None,
                       dc_input_capacity=None,
                       number_of_connected_combiners=99,
                       module_manufacturer='F'),
            InverterDO(name='INVERTER NAME 02',
                       iec_name='IEC NAME 02',
                       nominal_power_wac=333_333,
                       maximum_power_kwac=None,
                       total_dc_power=444_444,
                       states_and_fault_codes=None,
                       manufacturer='MANUFACTURER 02',
                       model='MODEL 02',
                       eventlist_name='EVENTLIST NAME 02',
                       umpp_min=100,
                       umpp_max=200,
                       dc_max_voltage=1_000,
                       dc_max_current=2_000,
                       dc_max_power=100_000,
                       dc_nameplate=200_000,
                       dc_peak_power=300_000,
                       firmware_version=None,
                       dc_input_capacity=None,
                       number_of_connected_combiners=99,
                       module_manufacturer='F'),
            InverterDO(name='INVERTER NAME 03',
                       iec_name='IEC NAME 03',
                       nominal_power_wac=555_555,
                       maximum_power_kwac=None,
                       total_dc_power=666_666,
                       states_and_fault_codes=None,
                       manufacturer='MANUFACTURER 03',
                       model='MODEL 03',
                       eventlist_name='EVENTLIST NAME 03',
                       umpp_min=100,
                       umpp_max=200,
                       dc_max_voltage=1_000,
                       dc_max_current=2_000,
                       dc_max_power=100_000,
                       dc_nameplate=200_000,
                       dc_peak_power=300_000,
                       firmware_version=None,
                       dc_input_capacity=None,
                       number_of_connected_combiners=99,
                       module_manufacturer='F')
        ]
        actual = self.controller.get_inverters(dataframe=dataframe, row_offset=0, rows=20)
        self.assertListEqual(expected, actual, 'Failed to assert expected InverterDO')

    def test_get_combiners(self):
        dataframe = pd.DataFrame(COMBINER_DATA)
        expected = [
            CombinerDO(name='COMBINER NAME 01',
                       iec_name='IEC NAME 01',
                       capacity_wdc=11_111,
                       manufacturer='MANUFACTURER 01',
                       model='MODEL 01',
                       temperature_coefficient=-0.0123,
                       contract_degradation_rate=0.0123,
                       manufacturer_degradation_rate=0.0456,
                       measured_degradation_rate=None),
            CombinerDO(name='COMBINER NAME 02',
                       iec_name='IEC NAME 02',
                       capacity_wdc=22_222,
                       manufacturer='MANUFACTURER 02',
                       model='MODEL 02',
                       temperature_coefficient=-0.0456,
                       contract_degradation_rate=0.0456,
                       manufacturer_degradation_rate=0.0789,
                       measured_degradation_rate=None),
            CombinerDO(name='COMBINER NAME 03',
                       iec_name='IEC NAME 03',
                       capacity_wdc=33_333,
                       manufacturer='MANUFACTURER 03',
                       model='MODEL 03',
                       temperature_coefficient=-0.9876,
                       contract_degradation_rate=0.5432,
                       manufacturer_degradation_rate=0.0100,
                       measured_degradation_rate=None)
        ]
        actual = self.controller.get_combiners(dataframe=dataframe, row_offset=0, rows=9)
        self.assertListEqual(expected, actual, 'Failed to assert expected CombinerDO')

    def test_get_site_level_non_elec(self):
        dataframe = pd.DataFrame(SITE_LEVEL_NON_ELEC_DATA)
        expected = [
            SiteLevelNonElecDO(number_of_met_stations=1,
                               number_of_soiling_stations=2)
        ]
        actual = self.controller.get_site_level_non_elec(dataframe=dataframe, row_offset=0, rows=3)
        self.assertListEqual(expected, actual, 'Failed to assert expected SiteLevelNonElecDO')

    def test_get_met_stations(self):
        dataframe = pd.DataFrame(MET_STATION_DATA)
        expected = [
            MetStationDO(name='MET STATION NAME 01',
                         iec_name='IEC NAME 01',
                         number_of_poa_sensors=1,
                         iec_pos_sensors='IEC POA SENSORS 01',
                         number_of_rear_facing_sensors=2,
                         number_of_irradiance_sensors=3,
                         number_of_ghi_sensors=4,
                         number_of_bom_temp_sensors=5,
                         iec_bom_temperature_sensors='IEC BOM TEMPERATURE 01',
                         number_of_ambient_temp_sensors=6),
            MetStationDO(name='MET STATION NAME 02',
                         iec_name='IEC NAME 02',
                         number_of_poa_sensors=2,
                         iec_pos_sensors='IEC POA SENSORS 02',
                         number_of_rear_facing_sensors=2,
                         number_of_irradiance_sensors=3,
                         number_of_ghi_sensors=4,
                         number_of_bom_temp_sensors=5,
                         iec_bom_temperature_sensors='IEC BOM TEMPERATURE 02',
                         number_of_ambient_temp_sensors=6),
            MetStationDO(name='MET STATION NAME 03',
                         iec_name='IEC NAME 03',
                         number_of_poa_sensors=3,
                         iec_pos_sensors='IEC POA SENSORS 03',
                         number_of_rear_facing_sensors=2,
                         number_of_irradiance_sensors=3,
                         number_of_ghi_sensors=4,
                         number_of_bom_temp_sensors=5,
                         iec_bom_temperature_sensors='IEC BOM TEMPERATURE 03',
                         number_of_ambient_temp_sensors=6)
        ]
        actual = self.controller.get_met_stations(dataframe=dataframe, row_offset=0, rows=10)
        self.assertListEqual(expected, actual, 'Failed to assert expected MetStationDO')

    def test_get_sensors(self):
        dataframe = pd.DataFrame(SENSOR_DATA)
        expected = [
            SensorDO(name='SENSOR NAME 01',
                     operating_range=None,
                     manufacturer='MANUFACTURER 01',
                     model='MODEL 01',
                     calibration_date=None,
                     calibration_value=None,
                     sensor_type='SENSOR TYPE 01'),
            SensorDO(name='SENSOR NAME 02',
                     operating_range=None,
                     manufacturer='MANUFACTURER 02',
                     model='MODEL 02',
                     calibration_date=None,
                     calibration_value=None,
                     sensor_type='SENSOR TYPE 02'),
            SensorDO(name='SENSOR NAME 03',
                     operating_range=None,
                     manufacturer='MANUFACTURER 03',
                     model='MODEL 03',
                     calibration_date=None,
                     calibration_value=None,
                     sensor_type='SENSOR TYPE 03')
        ]
        actual = self.controller.get_sensors(dataframe=dataframe, row_offset=0, rows=7)
        self.assertListEqual(expected, actual, 'Failed to assert expected SensorDO')

    # TODO: Change date data to date string of MM-DD-YYYY format
    def test_get_soiling_stations(self):
        dataframe = pd.DataFrame(SOILING_STATION_DATA)
        expected = [SoilingStationDO(name='SOILING STATION NAME',
                                     soiling_rate=0.012,
                                     last_cleaning_date=12345,
                                     last_calibration_date=56789)]
        actual = self.controller.get_soiling_stations(dataframe=dataframe, row_offset=0, rows=4)
        self.assertListEqual(expected, actual, 'Failed to assert expected SoilingStationDO')

    # TODO: Change either DO or test to accept correct tracker property types
    def test_get_trackers(self):
        dataframe = pd.DataFrame(TRACKER_DATA)
        expected = [
            TrackerDO(name='TRACKER NAME 01',
                      manufacturer='MANUFACTURER 01',
                      model='MODEL 01',
                      axis_orientation=1,
                      max_rotation_limit_east=1,
                      max_rotation_limit_west=1,
                      control_algorithm='CONTROL ALGORITHM 01',
                      modules_on_tracker_row=1,
                      modules_layout_on_trackers=1,
                      post_to_post_separation=1,
                      stow_position_snow=1,
                      stow_position_wind=1,
                      block=1,
                      assoc_electrical_pvps=1,
                      controller_number=1,
                      motor_number=1,
                      row_height=1,
                      modules_per_row=1,
                      rows_per_motor=1),
            TrackerDO(name='TRACKER NAME 02',
                      manufacturer='MANUFACTURER 02',
                      model='MODEL 02',
                      axis_orientation=2,
                      max_rotation_limit_east=2,
                      max_rotation_limit_west=2,
                      control_algorithm='CONTROL ALGORITHM 02',
                      modules_on_tracker_row=2,
                      modules_layout_on_trackers=2,
                      post_to_post_separation=2,
                      stow_position_snow=2,
                      stow_position_wind=2,
                      block=2,
                      assoc_electrical_pvps=2,
                      controller_number=2,
                      motor_number=2,
                      row_height=2,
                      modules_per_row=2,
                      rows_per_motor=2),
            TrackerDO(name='TRACKER NAME 03',
                      manufacturer='MANUFACTURER 03',
                      model='MODEL 03',
                      axis_orientation=3,
                      max_rotation_limit_east=3,
                      max_rotation_limit_west=3,
                      control_algorithm='CONTROL ALGORITHM 03',
                      modules_on_tracker_row=3,
                      modules_layout_on_trackers=3,
                      post_to_post_separation=3,
                      stow_position_snow=3,
                      stow_position_wind=3,
                      block=3,
                      assoc_electrical_pvps=3,
                      controller_number=3,
                      motor_number=3,
                      row_height=3,
                      modules_per_row=3,
                      rows_per_motor=3)
        ]
        actual = self.controller.get_trackers(dataframe=dataframe, row_offset=0, rows=19)
        self.assertListEqual(expected, actual, 'Failed to assert expected TrackerDO')

    def test_get_meter_box(self):
        dataframe = pd.DataFrame(METER_BOX_DATA)
        expected = [
            MeterBoxDO(name='METER BOX NAME',
                       iec_name='IEC NAME',
                       deeper_level_asset_ref='DEEPER LEVEL ASSET',
                       meterkind='METERKIND')
        ]
        actual = self.controller.get_meter_box(dataframe=dataframe, row_offset=0, rows=4)
        self.assertListEqual(expected, actual, 'Failed to assert expected MeterBoxDO')

    # TODO: Write validation test for self.controller._SiteCharacteristicsController__dataframe_to_worksheet


if __name__ == '__main__':
    unittest.main()
