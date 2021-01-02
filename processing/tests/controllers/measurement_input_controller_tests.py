import unittest

import pandas as pd
from pandas.testing import assert_frame_equal
from processing.measurement_input_controller import MeasurementInputController


class MeasurementInputControllerTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.met_station_dos = []
        self.controller = MeasurementInputController()

    def test_get_meas_input_dataframe_generates_empty_dataframe_from_empty_input(self):
        tag_list_dos = []
        measInput_data = {
            "Applicable to on-boarded site": [],
            "AssetType": [],
            "measurementType": [],
            "business_description": [],
            "LN_prefix": [],
            "LN_lnClass": [],
            "Max LN_inst": [],
            "DOName": [],
            "DAName": [],
            "dataFormat": [],
            "name_SIUnit": [],
            "MeasurementType": [],
            "IEC61850MeasurementReferential-qaqc_sequence": [],
            "IEC61850MeasurementReferential-qaqc_priority": [],
            "Analog-AnalogLimitSet": [],
            "Analog-DataSourceID": [],
            "tech_source_measurement_Rel-name_tech_source": [],
            "tech_source_measurement_Rel-data_time_zone": [],
            "tech_source_measurement_Rel-static_time_offset": [],
            "tech_source_measurement_Rel-rdl_connection_date": [],
            "tech_source_measurement_Rel-rdl_disconnection_date": [],
            "tech_source_measurement_Rel-template_switch_state_mapping": [],
            "raw_unit_symbol_automaticallyAvailable": [],
            "raw_unitMultiplier_value": [],
            "raw_unitSymbol_value": []
        }
        expected = pd.DataFrame(data=measInput_data, columns=measInput_data.keys(), dtype=object)
        actual = self.controller.get_measurements_dataframe(tag_list_dos=tag_list_dos)

        expected = expected.reindex_like(actual)
        assert_frame_equal(expected, actual)


if __name__ == '__main__':
    unittest.main()
