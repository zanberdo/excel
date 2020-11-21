class SiteLevelDO:

    def __init__(self, project_code, iec_bay_name, latitude, longitude, module_tilt, module_orientation,
                 capacity_limit_wac, total_capacity_wdc, number_of_feeders, cod):
        self.project_code = project_code
        self.iec_bay_name = iec_bay_name
        self.latitude = latitude
        self.longitude = longitude
        self.module_tilt = module_tilt
        self.module_orientation = module_orientation
        self.capacity_limit_wac = capacity_limit_wac
        self.total_capacity_wdc = total_capacity_wdc
        self.number_of_feeders = number_of_feeders
        self.doc = cod

    def __repr__(self) -> str:
        results = "SiteLevelDO{\n"
        for attr, value in self.__dict__.items():
            results += f"\t{attr}='{value}',\n"
        results += "}"
        return results
