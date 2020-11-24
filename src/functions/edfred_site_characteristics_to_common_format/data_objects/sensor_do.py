class SensorDO:

    def __init__(self,
                 name,
                 operating_range,
                 manufacturer,
                 model,
                 calibration_date,
                 calibration_value,
                 sensor_type):
        self.name = name
        self.operating_range = operating_range
        self.manufacturer = manufacturer
        self.model = model
        self.calibration_date = calibration_date
        self.calibration_value = calibration_value
        self.sensor_type = sensor_type

    def __repr__(self) -> str:
        results = '{\n\t"SensorDO" : {\n'
        for attr, value in self.__dict__.items():
            if type(value) is int:
                results += f'\t\t"{attr}": {value},\n'
            else:
                results += f'\t\t"{attr}": "{value}",\n'
        return results[:-2] + "\n\t}" + "\n}"
