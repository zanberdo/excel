import unittest
from datetime import datetime

import pandas as pd
from pandas.testing import assert_frame_equal

from processing.data_objects import CombinerDO
from processing.data_objects import InverterDO
from processing.data_objects import ShelterDO
from processing.electrical_input_controller import ElectricalInputController

ELECTRICAL_INPUT_DATA = {
    'Asset Ref Code': ['PROJ-TT00-I0-S00', 'PROJ-TT00-I0-S01', 'PROJ-TT00-I1-S00', 'PROJ-TT00-I1-S01',
                       'PROJ-TT01-I0-S00', 'PROJ-TT01-I0-S01', 'PROJ-TT01-I1-S00', 'PROJ-TT01-I1-S01'],
    'SHELTER SQL': ['PROJ-TT00', 'PROJ-TT00', 'PROJ-TT00', 'PROJ-TT00', 'PROJ-TT01', 'PROJ-TT01', 'PROJ-TT01',
                    'PROJ-TT01'],
    'INVERTER SQL': ['PROJ-TT00-I0', 'PROJ-TT00-I0', 'PROJ-TT00-I1', 'PROJ-TT00-I1', 'PROJ-TT01-I0', 'PROJ-TT01-I0',
                     'PROJ-TT01-I1', 'PROJ-TT01-I1'],
    'Cbox level B SQL': ['PROJ-TT00-I0-00', 'PROJ-TT00-I0-01', 'PROJ-TT00-I1-00', 'PROJ-TT00-I1-01', 'PROJ-TT01-I0-00',
                         'PROJ-TT01-I0-01', 'PROJ-TT01-I1-00', 'PROJ-TT01-I1-01'],
    'PARC SQL': ['PROJ', 'PROJ', 'PROJ', 'PROJ', 'PROJ', 'PROJ', 'PROJ', 'PROJ'],
    'Parc Basic Ref': ['PROJ_ECP001_S3', 'PROJ_ECP001_S3', 'PROJ_ECP001_S3', 'PROJ_ECP001_S3', 'PROJ_ECP001_S3',
                       'PROJ_ECP001_S3', 'PROJ_ECP001_S3', 'PROJ_ECP001_S3'],
    'Bay - AC': ['PROJ_ECP001_S3_SUB001LevHv01Upgrid01Cell', 'PROJ_ECP001_S3_SUB001LevHv01Upgrid01Cell',
                 'PROJ_ECP001_S3_SUB001LevHv01Upgrid01Cell', 'PROJ_ECP001_S3_SUB001LevHv01Upgrid01Cell',
                 'PROJ_ECP001_S3_SUB001LevHv01Upgrid01Cell', 'PROJ_ECP001_S3_SUB001LevHv01Upgrid01Cell',
                 'PROJ_ECP001_S3_SUB001LevHv01Upgrid01Cell', 'PROJ_ECP001_S3_SUB001LevHv01Upgrid01Cell'],
    'Feeder - AC': ['PROJ_ECP001_S3_SUB001LevMv01Feeder00Cell', 'PROJ_ECP001_S3_SUB001LevMv01Feeder00Cell',
                    'PROJ_ECP001_S3_SUB001LevMv01Feeder00Cell', 'PROJ_ECP001_S3_SUB001LevMv01Feeder00Cell',
                    'PROJ_ECP001_S3_SUB001LevMv01Feeder01Cell', 'PROJ_ECP001_S3_SUB001LevMv01Feeder01Cell',
                    'PROJ_ECP001_S3_SUB001LevMv01Feeder01Cell', 'PROJ_ECP001_S3_SUB001LevMv01Feeder01Cell'],
    'InverterStation - AC': ['PROJ_ECP001_S3_SHL000', 'PROJ_ECP001_S3_SHL000', 'PROJ_ECP001_S3_SHL000',
                             'PROJ_ECP001_S3_SHL000', 'PROJ_ECP001_S3_SHL001', 'PROJ_ECP001_S3_SHL001',
                             'PROJ_ECP001_S3_SHL001', 'PROJ_ECP001_S3_SHL001'],
    'ACDCConverter - AC/DC': ['PROJ_ECP001_S3_SHL000Inverter00', 'PROJ_ECP001_S3_SHL000Inverter00',
                              'PROJ_ECP001_S3_SHL000Inverter01', 'PROJ_ECP001_S3_SHL000Inverter01',
                              'PROJ_ECP001_S3_SHL001Inverter00', 'PROJ_ECP001_S3_SHL001Inverter00',
                              'PROJ_ECP001_S3_SHL001Inverter01', 'PROJ_ECP001_S3_SHL001Inverter01'],
    'CombinerBox A - DC': ['PROJ_ECP001_S3_SHL000_CA000', 'PROJ_ECP001_S3_SHL000_CA000', 'PROJ_ECP001_S3_SHL000_CA001',
                           'PROJ_ECP001_S3_SHL000_CA001', 'PROJ_ECP001_S3_SHL001_CA000', 'PROJ_ECP001_S3_SHL001_CA000',
                           'PROJ_ECP001_S3_SHL001_CA001', 'PROJ_ECP001_S3_SHL001_CA001'],
    'Dcbusbar A - DC': ['PROJ_ECP001_S3_SHL000_CA000_BBS000001', 'PROJ_ECP001_S3_SHL000_CA000_BBS000001',
                        'PROJ_ECP001_S3_SHL000_CA001_BBS000001', 'PROJ_ECP001_S3_SHL000_CA001_BBS000001',
                        'PROJ_ECP001_S3_SHL001_CA000_BBS000001', 'PROJ_ECP001_S3_SHL001_CA000_BBS000001',
                        'PROJ_ECP001_S3_SHL001_CA001_BBS000001', 'PROJ_ECP001_S3_SHL001_CA001_BBS000001'],
    'CombinerBox B - DC': ['PROJ_ECP001_S3_SHL000_CA000_CB000', 'PROJ_ECP001_S3_SHL000_CA000_CB001',
                           'PROJ_ECP001_S3_SHL000_CA001_CB000', 'PROJ_ECP001_S3_SHL000_CA001_CB001',
                           'PROJ_ECP001_S3_SHL001_CA000_CB000', 'PROJ_ECP001_S3_SHL001_CA000_CB001',
                           'PROJ_ECP001_S3_SHL001_CA001_CB000', 'PROJ_ECP001_S3_SHL001_CA001_CB001'],
    'Dcbusbar B - DC': ['PROJ_ECP001_S3_SHL000_CA000_CB000_BBS000001', 'PROJ_ECP001_S3_SHL000_CA000_CB001_BBS000001',
                        'PROJ_ECP001_S3_SHL000_CA001_CB000_BBS000001', 'PROJ_ECP001_S3_SHL000_CA001_CB001_BBS000001',
                        'PROJ_ECP001_S3_SHL001_CA000_CB000_BBS000001', 'PROJ_ECP001_S3_SHL001_CA000_CB001_BBS000001',
                        'PROJ_ECP001_S3_SHL001_CA001_CB000_BBS000001', 'PROJ_ECP001_S3_SHL001_CA001_CB001_BBS000001'],
    'Layer_ALL_Contractual': ['PROJ', 'PROJ', 'PROJ', 'PROJ', 'PROJ', 'PROJ', 'PROJ', 'PROJ'],
    'Layer_ALL_ISOGeographical': ['COUNTRY', 'COUNTRY', 'COUNTRY', 'COUNTRY', 'COUNTRY', 'COUNTRY', 'COUNTRY',
                                  'COUNTRY'],
    'Name_InverterStation_Contractual': ['PROJ-TT00', 'PROJ-TT00', 'PROJ-TT00', 'PROJ-TT00', 'PROJ-TT01', 'PROJ-TT01',
                                         'PROJ-TT01', 'PROJ-TT01'],
    'Name_ACDCConverter_Contractual': ['PROJ-TT00-I0', 'PROJ-TT00-I0', 'PROJ-TT00-I1', 'PROJ-TT00-I1', 'PROJ-TT01-I0',
                                       'PROJ-TT01-I0', 'PROJ-TT01-I1', 'PROJ-TT01-I1'],
    'Name_CombinerBoxB_Contractual': ['PROJ-TT00-I0-S00', 'PROJ-TT00-I0-S01', 'PROJ-TT00-I1-S00', 'PROJ-TT00-I1-S01',
                                      'PROJ-TT01-I0-S00', 'PROJ-TT01-I0-S01', 'PROJ-TT01-I1-S00', 'PROJ-TT01-I1-S01'],
    'Asset_ALL_InUseDate': ['2020-12-01', '2020-12-01', '2020-12-01', '2020-12-01', '2020-12-01', '2020-12-01',
                            '2020-12-01', '2020-12-01'],
    'PAM_CombinerBoxB_DCPeakPower': [0.011111, 0.011111, 0.011111, 0.011111, 0.011111, 0.011111, 0.011111, 0.011111],
    'PAM_CombinerBoxB_tempCoeffNemplate_value': [-0.00123, -0.00123, -0.00123, -0.00123, -0.00123, -0.00123, -0.00123,
                                                 -0.00123],
    'PAM_InverterRef': ['MANUFACTURER_MODEL', 'MANUFACTURER_MODEL', 'MANUFACTURER_MODEL', 'MANUFACTURER_MODEL',
                        'MANUFACTURER_MODEL', 'MANUFACTURER_MODEL', 'MANUFACTURER_MODEL', 'MANUFACTURER_MODEL']
}


class ElectricalInputControllerTests(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        self.controller = ElectricalInputController(project_code='PROJ', country='COUNTRY',
                                                    cod=datetime(year=2020, month=12, day=1))
        self.shelter_dos = []
        for i in range(2):
            self.shelter_dos.append(
                ShelterDO(
                    name=f'TT{i:02d}',
                    iec_name=f'PROJ_ECP001_S3_SHL{i:03d}',
                    capacity_wac=1_000_000,
                    capacity_wdc=1_200_000,
                    number_of_inverters_per_shelter=2,
                    parent_feeder=f'PROJ_ECP001_S3_SUB001LevMv01Feeder{i:02d}Cell'
                )
            )
        self.inverter_dos = []
        for i in range(2):
            for j in range(2):
                self.inverter_dos.append(
                    InverterDO(
                        name=f'TT{i:02d}-I{j}',
                        iec_name=f'PROJ_ECP001_S3_SHL{i:03d}Inverter{j:02d}',
                        nominal_power_wac=111_111,
                        maximum_power_kwac=None,
                        total_dc_power=222_222,
                        states_and_fault_codes=None,
                        manufacturer='MANUFACTURER',
                        model='MODEL',
                        eventlist_name='TST TS-20',
                        umpp_min=100,
                        umpp_max=200,
                        dc_max_voltage=1_000,
                        dc_max_current=2_000,
                        dc_max_power=100_000,
                        dc_nameplate=200_000,
                        dc_peak_power=300_000,
                        firmware_version=None,
                        dc_input_capacity=None,
                        number_of_connected_combiners=3,
                        module_manufacturer='X'
                    )
                )
        self.combiner_dos = []
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    self.combiner_dos.append(
                        CombinerDO(
                            name=f'TT{i:02d}-I{j}-{k:02d}',
                            iec_name=f'PROJ_ECP001_S3_SHL{i:03d}_CA{j:03d}_CB{k:03d}',
                            capacity_wdc=11_111,
                            manufacturer=f'MANUFACTURER {i:02d}',
                            model=f'MODEL {i:02d}',
                            temperature_coefficient=-0.00123,
                            contract_degradation_rate=0.00123,
                            manufacturer_degradation_rate=0.0012,
                            measured_degradation_rate=None
                        )
                    )

    def test_get_electrical_input_dataframe(self):
        expected = pd.DataFrame(ELECTRICAL_INPUT_DATA)
        actual = self.controller.get_electrical_dataframe(combiner_dos=self.combiner_dos,
                                                          inverter_dos=self.inverter_dos,
                                                          shelter_dos=self.shelter_dos)
        assert_frame_equal(expected, actual)

    def test_get_electrical_input_dataframe_missing_shelter_throws_exception(self):
        shelter_dos = [ShelterDO(
            name='TT00',
            iec_name='PROJ_ECP001_S3_SHL999',
            capacity_wac=1_000_000,
            capacity_wdc=1_200_000,
            number_of_inverters_per_shelter=2,
            parent_feeder='PROJ_ECP001_S3_SUB001LevMv01Feeder00Cell'
        )]
        inverter_dos = [InverterDO(
            name='TT00-I0',
            iec_name='PROJ_ECP001_S3_SHL999Inverter00',
            nominal_power_wac=111_111,
            maximum_power_kwac=None,
            total_dc_power=222_222,
            states_and_fault_codes=None,
            manufacturer='MANUFACTURER',
            model='MODEL',
            eventlist_name='TST TS-20',
            umpp_min=100,
            umpp_max=200,
            dc_max_voltage=1_000,
            dc_max_current=2_000,
            dc_max_power=100_000,
            dc_nameplate=200_000,
            dc_peak_power=300_000,
            firmware_version=None,
            dc_input_capacity=None,
            number_of_connected_combiners=3,
            module_manufacturer='X'
        )]
        combiner_dos = [CombinerDO(
            name='TT00-I0-00',
            iec_name='PROJ_ECP001_S3_SHL000_CA000_CB000',
            capacity_wdc=11_111,
            manufacturer='MANUFACTURER',
            model='MODEL',
            temperature_coefficient=-0.00123,
            contract_degradation_rate=0.00123,
            manufacturer_degradation_rate=0.0012,
            measured_degradation_rate=None
        )]
        with self.assertRaises(Exception):
            self.controller.get_electrical_dataframe(combiner_dos=combiner_dos,
                                                     inverter_dos=inverter_dos,
                                                     shelter_dos=shelter_dos)

    def test_get_electrical_input_dataframe_missing_inverter_throws_exception(self):
        shelter_dos = [ShelterDO(
            name='TT00',
            iec_name='PROJ_ECP001_S3_SHL000',
            capacity_wac=1_000_000,
            capacity_wdc=1_200_000,
            number_of_inverters_per_shelter=2,
            parent_feeder='PROJ_ECP001_S3_SUB001LevMv01Feeder00Cell'
        )]
        inverter_dos = [InverterDO(
            name='TT00-I0',
            iec_name='PROJ_ECP001_S3_SHL999Inverter00',
            nominal_power_wac=111_111,
            maximum_power_kwac=None,
            total_dc_power=222_222,
            states_and_fault_codes=None,
            manufacturer='MANUFACTURER',
            model='MODEL',
            eventlist_name='TST TS-20',
            umpp_min=100,
            umpp_max=200,
            dc_max_voltage=1_000,
            dc_max_current=2_000,
            dc_max_power=100_000,
            dc_nameplate=200_000,
            dc_peak_power=300_000,
            firmware_version=None,
            dc_input_capacity=None,
            number_of_connected_combiners=3,
            module_manufacturer='X'
        )]
        combiner_dos = [CombinerDO(
            name='TT00-I0-00',
            iec_name='PROJ_ECP001_S3_SHL000_CA000_CB000',
            capacity_wdc=11_111,
            manufacturer='MANUFACTURER',
            model='MODEL',
            temperature_coefficient=-0.00123,
            contract_degradation_rate=0.00123,
            manufacturer_degradation_rate=0.0012,
            measured_degradation_rate=None
        )]
        with self.assertRaises(Exception):
            self.controller.get_electrical_dataframe(combiner_dos=combiner_dos,
                                                     inverter_dos=inverter_dos,
                                                     shelter_dos=shelter_dos)


if __name__ == '__main__':
    unittest.main()
