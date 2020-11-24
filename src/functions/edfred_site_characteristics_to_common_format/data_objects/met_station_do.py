class MetStationDO:

    def __init__(self,
                 name,
                 iec_name,
                 number_of_poa_sensors,
                 iec_number_of_poa_sensors,
                 number_of_ghi_sensors,
                 number_of_back_of_module_temperatures,
                 number_of_ambient_temperatures):
        self.name = name
        self.iec_name = iec_name
        self.number_of_poa_sensors = number_of_poa_sensors
        self.iec_number_of_poa_sensors = iec_number_of_poa_sensors
        self.number_of_ghi_sensors = number_of_ghi_sensors
        self.number_of_back_of_module_temperatures = number_of_back_of_module_temperatures
        self.number_of_ambient_temperatures = number_of_ambient_temperatures


def __repr__(self) -> str:
    results = '{\n\t"MetStationDO" : {\n'
    for attr, value in self.__dict__.items():
        if type(value) is int:
            results += f'\t\t"{attr}": {value},\n'
        else:
            results += f'\t\t"{attr}": "{value}",\n'
    return results[:-2] + "\n\t}" + "\n}"
