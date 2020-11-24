class SiteLevelNonElecDO:

    def __init__(self,
                 number_of_met_stations,
                 number_of_soiling_stations):
        self.number_of_met_stations = number_of_met_stations
        self.number_of_soiling_stations = number_of_soiling_stations

    def __repr__(self) -> str:
        results = '{\n\t"SiteLevelNonElecDO" : {\n'
        for attr, value in self.__dict__.items():
            if type(value) is int:
                results += f'\t\t"{attr}": {value},\n'
            else:
                results += f'\t\t"{attr}": "{value}",\n'
        return results[:-2] + "\n\t}" + "\n}"
