import unittest

from src.functions.lambdas.edfred_solar_site_onboarding_to_common_format.data_objects import InverterDO


class InverterDOTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self) -> None:
        pass

    def test_unique_hash(self):
        inverter_dos = [InverterDO(
            name='INVERTER 01',
            iec_name='INVERTER IEC NAME 01',
            nominal_power_wac=75_000,
            maximum_power_kwac=80,
            total_dc_power=100_000,
            states_and_fault_codes=None,
            manufacturer='INVERTER MANUFACTURER 01',
            model='INVERTER MODEL 01',
            eventlist_name='INVERTER EVENTLIST NAME 01',
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
        ), InverterDO(
            name='INVERTER 02',
            iec_name='INVERTER IEC NAME 02',
            nominal_power_wac=100_000,
            maximum_power_kwac=80,
            total_dc_power=100_000,
            states_and_fault_codes=None,
            manufacturer='INVERTER MANUFACTURER 02',
            model='INVERTER MODEL 02',
            eventlist_name='INVERTER EVENTLIST NAME 02',
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
        ), InverterDO(
            name='INVERTER 03',
            iec_name='INVERTER IEC NAME 03',
            nominal_power_wac=75_000,
            maximum_power_kwac=80,
            total_dc_power=100_000,
            states_and_fault_codes=None,
            manufacturer='INVERTER MANUFACTURER 01',
            model='INVERTER MODEL 01',
            eventlist_name='INVERTER EVENTLIST NAME 03',
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
        expected_inverter_hash_len = len(inverter_dos)
        expected_inverter_unique_hash_len = 2
        expected_unique_inverters = {inverter_dos[0].get_unique_hash(): inverter_dos[0],
                                     inverter_dos[1].get_unique_hash(): inverter_dos[1]}

        actual_inverter_hashes = set()
        actual_inverter_unique_hashes = set()
        actual_unique_inverters = {}

        for inverter_do in inverter_dos:
            actual_inverter_hashes.add(hash(inverter_do))
            if inverter_do.get_unique_hash() not in actual_inverter_unique_hashes:
                actual_inverter_unique_hashes.add(inverter_do.get_unique_hash())
                actual_unique_inverters[inverter_do.get_unique_hash()] = inverter_do

        self.assertEqual(expected_inverter_hash_len, len(actual_inverter_hashes),
                         'Actual number of inverter hashes does not match expected number of hashes')
        self.assertEqual(expected_inverter_unique_hash_len, len(actual_inverter_unique_hashes),
                         'Actual number of unique inverter hashes does not match expected number of unique hashes')
        self.assertDictEqual(expected_unique_inverters, actual_unique_inverters,
                             'Actual unique inverters does not match expected unique inverters')


if __name__ == '__main__':
    unittest.main()
