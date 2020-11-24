class InverterDO:

    def __init__(self,
                 name,
                 iec_name,
                 nominal_power_wac,
                 maximum_power_kwac,
                 total_dc_power,
                 states_and_fault_codes,
                 manufacturer,
                 model,
                 firmware_version,
                 dc_input_capacity,
                 number_of_connected_combiners,
                 module_manufacturer):
        self.name = name
        self.iec_name = iec_name
        self.nominal_power_wac = nominal_power_wac
        self.maximum_power_kwac = maximum_power_kwac
        self.total_dc_power = total_dc_power
        self.states_and_fault_codes = states_and_fault_codes
        self.manufacturer = manufacturer
        self.model = model
        self.firmware_version = firmware_version
        self.dc_input_capacity = dc_input_capacity
        self.number_of_connected_combiners = number_of_connected_combiners
        self.module_manufacturer = module_manufacturer

    def __repr__(self) -> str:
        results = '{\n\t"InverterDO" : {\n'
        for attr, value in self.__dict__.items():
            if type(value) is int:
                results += f'\t\t"{attr}": {value},\n'
            else:
                results += f'\t\t"{attr}": "{value}",\n'
        return results[:-2] + "\n\t}" + "\n}"
