class CombinerDO:

    def __init__(self,
                 name,
                 iec_combiner_name,
                 capacity_wcd,
                 manufacturer_and_model,
                 temperature_coefficient,
                 contract_degradation_rate,
                 manufacturer_degradation_rate,
                 measured_degradation_rate):
        self.name = name
        self.iec_combiner_name = iec_combiner_name
        self.capacity_wcd = capacity_wcd
        self.manufacturer_and_model = manufacturer_and_model
        self.temperature_coefficient = temperature_coefficient
        self.contract_degradation_rate = contract_degradation_rate
        self.manufacturer_degradation_rate = manufacturer_degradation_rate
        self.measure_degradation_rate = measured_degradation_rate

    def __repr__(self) -> str:
        results = '{\n\t"CombinerDO" : {\n'
        for attr, value in self.__dict__.items():
            if type(value) is int:
                results += f'\t\t"{attr}": {value},\n'
            else:
                results += f'\t\t"{attr}": "{value}",\n'
        return results[:-2] + "\n\t}" + "\n}"
