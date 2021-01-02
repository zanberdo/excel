import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from processing.asset_list_input_controller import AssetListInputController
from processing.data_objects import CombinerDO

COMBINER_BOX_INPUT_DATA = {
    'AssetInput': ['TT00-I0-00', 'TT00-I0-01', 'TT00-I1-00', 'TT00-I1-01', 'TT01-I0-00', 'TT01-I0-01', 'TT01-I1-00',
                   'TT01-I1-01'],
    'AssetInfo_CombinerBoxB_DCPeakPower': [11_111, 11_111, 11_111, 11_111, 11_111, 11_111, 11_111, 11_111]
}


class AssetListInputControllerTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.controller = AssetListInputController()
        self.combiner_dos = []
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    self.combiner_dos.append(
                        CombinerDO(
                            name=f'TT{i:02d}-I{j}-{k:02d}',
                            iec_name=f'TEST_ECP001_S3_SHL{i:03d}_CA{j:03d}_CB{k:03d}',
                            capacity_wdc=11_111,
                            manufacturer=f'MANUFACTURER {i:02d}',
                            model=f'MODEL {i:02d}',
                            temperature_coefficient=-0.00123,
                            contract_degradation_rate=0.00123,
                            manufacturer_degradation_rate=0.0012,
                            measured_degradation_rate=None
                        )
                    )

    def test_get_asset_list_input_dataframe(self):
        expected = pd.DataFrame(COMBINER_BOX_INPUT_DATA)
        actual = self.controller.get_asset_list_dataframe(combiner_dos=self.combiner_dos)
        assert_frame_equal(expected, actual)


if __name__ == '__main__':
    unittest.main()
