class SoilingStationDO:

    def __init__(self,
                 name,
                 soiling_rate,
                 last_cleaning_date,
                 last_calibration_date):
        self.name = name
        self.soling_rate = soiling_rate
        self.last_cleaning_date = last_cleaning_date
        self.last_calibration_date = last_calibration_date

    def __repr__(self) -> str:
        results = '{\n\t"SoilingStationDO" : {\n'
        for attr, value in self.__dict__.items():
            if type(value) is int:
                results += f'\t\t"{attr}": {value},\n'
            else:
                results += f'\t\t"{attr}": "{value}",\n'
        return results[:-2] + "\n\t}" + "\n}"
