class FeederDO:

    def __init__(self, name, iec_name, capacity_wac, capacity_wdc,
                 number_of_shelters_inverters,
                 cod, contract_project_code):
        self.name = name
        self.iec_name = iec_name
        self.feeder_capacity_wac = capacity_wac
        self.feeder_capacity_wdc = capacity_wdc
        self.number_of_shelters_inverters = number_of_shelters_inverters
        self.cod = cod
        self.contract_project_code = contract_project_code

    def __repr__(self) -> str:
        results = '{\n\t"FeederDO" : {\n'
        for attr, value in self.__dict__.items():
            if type(value) is int:
                results += f'\t\t"{attr}": {value},\n'
            else:
                results += f'\t\t"{attr}": "{value}",\n'
        results = results[:-2] + "\n\t}" + "\n}"
        return results
