import pandas as pd
from openpyxl.workbook.workbook import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from functions.edfred_site_characteristics_to_common_format.data_objects.feeder_do import FeederDO
from functions.edfred_site_characteristics_to_common_format.data_objects.inverter_do import InverterDO
from functions.edfred_site_characteristics_to_common_format.data_objects.shelter_do import ShelterDO
from functions.edfred_site_characteristics_to_common_format.data_objects.site_level_do import SiteLevelDO

SITE_CHAR_FILE = "/Users/mark.zanfardino/Documents/SD-1359/global checklist for solar site onboarding_BOUL.xlsx"


class Main:
    def __init__(self, src_checklist):
        self.src_checklist = src_checklist
        self.site_characteristic = "Site characteristic"
        self.tag_list_requirements = "Tag list requirements"

    def run(self):
        workbook = pd.ExcelFile(self.src_checklist)
        worksheet = [i for i in workbook.sheet_names if self.site_characteristic in i]
        if worksheet[0] in workbook.sheet_names:
            site_characteristics = workbook.parse(sheet_name=worksheet[0], header=None)
            site_level_do = self.get_site_level(site_characteristics, 4, 14, 3, 4)
            feeder_do = self.get_feeder(site_characteristics, 15, 22, 3, 4)
            shelter_dos = []
            # TODO: determine how many shelters exist in site char and build dos from that
            for i in range(0, 6):
                shelter_dos.append(self.get_shelter(site_characteristics, 23, 29, 3 + i, 4 + i))
            inverter_dos = []
            for col in range(3, 16):
                inverter_dos.append(self.get_inverter(site_characteristics, 30, 42, col, col + 1))
        else:
            raise (Exception(f"Failed to find worksheet: [{worksheet[0]}] in workbook. "
                             f"Worksheets: {workbook.sheet_names}"))

        print(repr(site_level_do) + ',')
        print(repr(feeder_do) + ',')
        for shelter_do in shelter_dos:
            print(repr(shelter_do) + ',')
        for inverter_do in inverter_dos:
            print(repr(inverter_do) + ',')

    def get_site_level(self, dataframe, row_start, row_end, col_start, col_end):
        worksheet = self.__dataframe_to_worksheet(col_end, col_start, dataframe, row_end, row_start)
        return SiteLevelDO(project_code=worksheet[1][0].value,
                           iec_bay_name=worksheet[2][0].value,
                           latitude=worksheet[3][0].value,
                           longitude=worksheet[4][0].value,
                           module_tilt=worksheet[5][0].value,
                           module_orientation=worksheet[6][0].value,
                           capacity_limit_wac=worksheet[7][0].value,
                           total_capacity_wdc=worksheet[8][0].value,
                           number_of_feeders=worksheet[9][0].value,
                           cod=worksheet[10][0].value)

    def get_feeder(self, dataframe, row_start, row_end, col_start, col_end):
        worksheet = self.__dataframe_to_worksheet(col_end, col_start, dataframe, row_end, row_start)
        return FeederDO(name=worksheet[1][0].value,
                        iec_name=worksheet[2][0].value,
                        capacity_wac=worksheet[3][0].value,
                        capacity_wdc=worksheet[4][0].value,
                        number_of_shelters_inverters=worksheet[5][0].value,
                        cod=worksheet[6][0].value,
                        contract_project_code=worksheet[7][0].value)

    def get_shelter(self, dataframe, row_start, row_end, col_start, col_end):
        worksheet = self.__dataframe_to_worksheet(col_end, col_start, dataframe, row_end, row_start)
        return ShelterDO(name=worksheet[1][0].value,
                         iec_shelter_name=worksheet[2][0].value,
                         capacity_wac=worksheet[3][0].value,
                         capacity_wdc=worksheet[4][0].value,
                         number_of_inverters_per_shelter=worksheet[5][0].value,
                         parent_feeder=worksheet[6][0].value)

    def get_inverter(self, dataframe, row_start, row_end, col_start, col_end):
        worksheet = self.__dataframe_to_worksheet(col_end, col_start, dataframe, row_end, row_start)
        return InverterDO(name=worksheet[1][0].value,
                          iec_inverter_name=worksheet[2][0].value,
                          nominal_power_wac=worksheet[3][0].value,
                          maximum_power_kwac=worksheet[4][0].value,
                          total_dc_power=worksheet[5][0].value,
                          states_and_fault_codes=worksheet[6][0].value,
                          manufacturer=worksheet[7][0].value,
                          model=worksheet[8][0].value,
                          firmware_version=worksheet[9][0].value,
                          dc_input_capacity=worksheet[10][0].value,
                          number_of_connected_combiners=worksheet[11][0].value,
                          module_manufacturer=worksheet[12][0].value
                          )

    def __dataframe_to_worksheet(self, col_end, col_start, dataframe, row_end, row_start):
        dataframe = dataframe.iloc[row_start:row_end][list(dataframe.columns[col_start:col_end])]
        worksheet = Workbook().create_sheet()
        for row in dataframe_to_rows(dataframe, index=False, header=False):
            worksheet.append(row)
        return worksheet


if __name__ == '__main__':
    main = Main(SITE_CHAR_FILE)
    main.run()
