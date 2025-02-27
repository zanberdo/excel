class SiteLevelDO:

    def __init__(self,
                 project_code,
                 iec_name,
                 latitude,
                 longitude,
                 module_tilt,
                 module_orientation,
                 capacity_limit_wac,
                 total_capacity_wdc,
                 number_of_feeders,
                 cod):
        self.project_code = project_code
        self.iec_name = iec_name
        self.latitude = latitude
        self.longitude = longitude
        self.module_tilt = module_tilt
        self.module_orientation = module_orientation
        self.capacity_limit_wac = capacity_limit_wac
        self.total_capacity_wdc = total_capacity_wdc
        self.number_of_feeders = number_of_feeders
        self.cod = cod

    def __repr__(self) -> str:
        results = '{\n\t"SiteLevelDO" : {\n'
        for attr, value in self.__dict__.items():
            if type(value) is int:
                results += f'\t\t"{attr}": {value},\n'
            else:
                results += f'\t\t"{attr}": "{value}",\n'
        return results[:-2] + "\n\t}" + "\n}"
