class MeterBoxDO:

    def __init__(self,
                 name,
                 iec_name,
                 deeper_level_asset_ref,
                 meterkind):
        self.name = name
        self.iec_name = iec_name
        self.deeper_level_asset_ref = deeper_level_asset_ref
        self.meterkind = meterkind

    def __repr__(self) -> str:
        results = '{\n\t"MeterBoxDO" : {\n'
        for attr, value in self.__dict__.items():
            if type(value) is int:
                results += f'\t\t"{attr}": {value},\n'
            else:
                results += f'\t\t"{attr}": "{value}",\n'
        return results[:-2] + "\n\t}" + "\n}"
