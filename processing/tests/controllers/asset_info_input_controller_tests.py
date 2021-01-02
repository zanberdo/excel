import logging
import os
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from processing.asset_info_input_controller import AssetInfoInputController
from processing.data_objects import CombinerDO
from processing.data_objects import InverterDO

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

realpath = os.path.split(__file__)[0]
logger.debug(f'Importing from: {realpath}')

# TODO: Write test that validates unique assets from both feeders and combiners
ASSET_INFO_INPUT_DATA = {
    'modelNumber': [],
    'modelVersion': [],
    'description': [],
    'name': [],
    'catalogueNumber': [],
    'instructionManual': [],
    'UmppMin_value': [],
    'UmppMax_value': [],
    'DCMaxVoltage_value': [],
    'DCMaxCurrent_value': [],
    'DCMaxPower_value': [],
    'DCNameplate_value': [],
    'tempCoeffNameplate_value': [],
    'DCPeakPower_value': [],
    'ACMaxPower_value': [],
    'ACNameplate_value': [],
    'manufacturer': [],
    'EventList_name': []
}


@unittest.skip("Skipping tests until properly constructed dataset completed")
class AssetInfoInputControllerTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.controller = AssetInfoInputController()
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
                        firmware_version=None,
                        dc_input_capacity=None,
                        number_of_connected_combiners=3,
                        module_manufacturer='X',
                        umpp_min=None,
                        umpp_max=None,
                        dc_max_voltage=None,
                        dc_max_current=None,
                        dc_max_power=None,
                        dc_nameplate=None,
                        dc_peak_power=None
                    )
                )

    # TODO: Figure out how to mock: controller.get_asset_info_dataframe.__init__ self.manufacturer_trigram
    def test_get_asset_info_input_dataframe(self):
        expected = pd.DataFrame(ASSET_INFO_INPUT_DATA)
        actual = self.controller.get_asset_info_dataframe(combiner_dos=self.combiner_dos,
                                                          inverter_dos=self.inverter_dos)
        assert_frame_equal(expected, actual)


if __name__ == '__main__':
    unittest.main()
