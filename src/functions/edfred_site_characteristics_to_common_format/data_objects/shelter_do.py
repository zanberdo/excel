class ShelterDO:

    def __init__(self, name, iec_shelter_name, capacity_wac, capacity_wdc, number_of_inverters_per_shelter,
                 parent_feeder):
        self.name = name
        self.iec_shelter_name = iec_shelter_name
        self.capacity_wac = capacity_wdc
        self.capacity_wdc = capacity_wac
        self.number_of_inverters_per_shelter = number_of_inverters_per_shelter
        self.parent_feeder = parent_feeder

    def __repr__(self) -> str:
        results = '{\n\t"ShelterDO" : {\n'
        for attr, value in self.__dict__.items():
            if type(value) is int:
                results += f'\t\t"{attr}": {value},\n'
            else:
                results += f'\t\t"{attr}": "{value}",\n'
        return results[:-2] + "\n\t}" + "\n}"
