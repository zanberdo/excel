from openpyxl.reader.excel import load_workbook

from functions.edfred_site_characteristics_to_common_format.data_objects.feeder_do import FeederDO
from functions.edfred_site_characteristics_to_common_format.data_objects.site_level_do import SiteLevelDO

SITE_CHAR_FILE = "/Users/mark.zanfardino/Documents/SD-1359/global checklist for solar site onboarding_BOUL.xlsx"
SHEET = 'DH1'


class Main:
    def __init__(self, src_checklist):
        self.src_checklist = src_checklist
        self.site_characteristic = "Site characteristic"
        self.tag_list_requirements = "Tag list requirements"

    def run(self):
        workbook = load_workbook(self.src_checklist, read_only=True, data_only=True)
        # Worksheet name appears to contain trailing space. The following will find a matching worksheet name without
        # concern for leading/trailing spaces and return the valid worksheet name with padding as found
        worksheet = [i for i in workbook.sheetnames if self.site_characteristic in i]
        if worksheet[0] in workbook.sheetnames:
            site_characteristic = workbook[worksheet[0]]
            site_level_do = self.get_site_level(site_characteristic)
            print(repr(site_level_do))
            feeder_do = self.get_feeder(site_characteristic)
            print(repr(feeder_do))
        else:
            raise(Exception(f"Failed to find worksheet: [{worksheet[0]}] in workbook. "
                            f"Worksheets: {workbook.sheetnames}"))

    def get_site_level(self, worksheet):
        return SiteLevelDO(project_code=worksheet['D5'].value,
                           iec_bay_name=worksheet['D6'].value,
                           latitude=worksheet['D7'].value,
                           longitude=worksheet['D8'].value,
                           module_tilt=worksheet['D9'].value,
                           module_orientation=worksheet['D10'].value,
                           capacity_limit_wac=worksheet['D11'].value,
                           total_capacity_wdc=worksheet['D12'].value,
                           number_of_feeders=worksheet['D13'].value,
                           cod=worksheet['D14'].value)

    def get_feeder(self, worksheet):

        return FeederDO(name=worksheet['D16'].value,
                        iec_name=worksheet['D17'].value,
                        capacity_wac=worksheet['D18'].value,
                        capacity_wdc=worksheet['D19'].value,
                        number_of_shelters_inverters=worksheet['D20'].value,
                        cod=worksheet['D21'].value,
                        contract_project_code=worksheet['D22'].value)


if __name__ == '__main__':
    main = Main(SITE_CHAR_FILE)
    main.run()
