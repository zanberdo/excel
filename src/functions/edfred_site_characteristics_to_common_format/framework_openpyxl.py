import math

import pandas as pd
from openpyxl.workbook.workbook import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from functions.edfred_site_characteristics_to_common_format.data_objects.combiner_do import CombinerDO
from functions.edfred_site_characteristics_to_common_format.data_objects.feeder_do import FeederDO
from functions.edfred_site_characteristics_to_common_format.data_objects.inverter_do import InverterDO
from functions.edfred_site_characteristics_to_common_format.data_objects.met_station_do import MetStationDO
from functions.edfred_site_characteristics_to_common_format.data_objects.meter_box_do import MeterBoxDO
from functions.edfred_site_characteristics_to_common_format.data_objects.sensor_do import SensorDO
from functions.edfred_site_characteristics_to_common_format.data_objects.shelter_do import ShelterDO
from functions.edfred_site_characteristics_to_common_format.data_objects.site_level_do import SiteLevelDO

# TODO: Replace hard-coded local file with S3 bucket object
from functions.edfred_site_characteristics_to_common_format.data_objects.site_level_non_elec_do import \
    SiteLevelNonElecDO
from functions.edfred_site_characteristics_to_common_format.data_objects.soiling_station_do import SoilingStationDO
from functions.edfred_site_characteristics_to_common_format.data_objects.tracker_do import TrackerDO

SITE_CHAR_FILE = "/Users/mark.zanfardino/Documents/SD-1359/global checklist for solar site onboarding_BOUL.xlsx"
DATA_COLUMN = 3


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
            site_level_dos = self.get_site_level(site_characteristics, row_start=4, row_end=14)
            feeder_dos = self.get_feeders(site_characteristics, row_start=15, row_end=22)
            shelter_dos = self.get_shelters(site_characteristics, row_start=23, row_end=29)
            inverter_dos = self.get_inverters(site_characteristics, row_start=30, row_end=42)
            combiner_dos = self.get_combiners(site_characteristics, row_start=44, row_end=52)
            site_level_non_elec_dos = self.get_site_level_non_elec(site_characteristics, row_start=59, row_end=61)
            met_station_dos = self.get_met_stations(site_characteristics, row_start=62, row_end=70)
            sensor_dos = self.get_sensors(site_characteristics, row_start=71, row_end=78)
            soiling_station_dos = self.get_soiling_stations(site_characteristics, row_start=79, row_end=83)
            tracker_dos = self.get_trackers(site_characteristics, row_start=84, row_end=103)
            meter_box_dos = self.get_meter_box(site_characteristics, row_start=105, row_end=108)

        else:
            raise (Exception(f"Failed to find worksheet: [{worksheet[0]}] in workbook. "
                             f"Worksheets: {workbook.sheet_names}"))

        print(repr(site_level_dos) + ',')
        print(repr(feeder_dos) + ',')
        print(repr(shelter_dos) + ',')
        print(repr(inverter_dos) + ',')
        print(repr(combiner_dos) + ',')
        print(repr(site_level_non_elec_dos) + ',')
        print(repr(met_station_dos) + ',')
        print(repr(sensor_dos) + ',')
        print(repr(soiling_station_dos) + ',')
        print(repr(tracker_dos) + ',')
        print(repr(meter_box_dos))

    # TODO: move these to persistence controller
    def get_site_level(self, dataframe, row_start, row_end):
        results = []
        for col in range(DATA_COLUMN, len(dataframe.columns)):
            worksheet = self.__dataframe_to_worksheet(dataframe=dataframe,
                                                      row_start=row_start,
                                                      row_end=row_end,
                                                      col_start=col,
                                                      col_end=col + 1)
            if self.__is_column_empty(worksheet):
                break
            results.append(SiteLevelDO(project_code=worksheet[1][0].value,
                                       iec_name=worksheet[2][0].value,
                                       latitude=worksheet[3][0].value,
                                       longitude=worksheet[4][0].value,
                                       module_tilt=worksheet[5][0].value,
                                       module_orientation=worksheet[6][0].value,
                                       capacity_limit_wac=worksheet[7][0].value,
                                       total_capacity_wdc=worksheet[8][0].value,
                                       number_of_feeders=worksheet[9][0].value,
                                       cod=worksheet[10][0].value)
                           )
        return results

    def get_feeders(self, dataframe, row_start, row_end):
        results = []
        for col in range(DATA_COLUMN, len(dataframe.columns)):
            worksheet = self.__dataframe_to_worksheet(dataframe=dataframe,
                                                      row_start=row_start,
                                                      row_end=row_end,
                                                      col_start=col,
                                                      col_end=col + 1)
            if self.__is_column_empty(worksheet):
                break
            results.append(FeederDO(name=worksheet[1][0].value,
                                    iec_name=worksheet[2][0].value,
                                    capacity_wac=worksheet[3][0].value,
                                    capacity_wdc=worksheet[4][0].value,
                                    number_of_shelters_inverters=worksheet[5][0].value,
                                    cod=worksheet[6][0].value,
                                    contract_project_code=worksheet[7][0].value)
                           )
        return results

    def get_shelters(self, dataframe, row_start, row_end):
        results = []
        for col in range(DATA_COLUMN, len(dataframe.columns)):
            worksheet = self.__dataframe_to_worksheet(dataframe=dataframe,
                                                      row_start=row_start,
                                                      row_end=row_end,
                                                      col_start=col,
                                                      col_end=col + 1)
            if self.__is_column_empty(worksheet):
                break
            results.append(ShelterDO(name=worksheet[1][0].value,
                                     iec_name=worksheet[2][0].value,
                                     capacity_wac=worksheet[3][0].value,
                                     capacity_wdc=worksheet[4][0].value,
                                     number_of_inverters_per_shelter=worksheet[5][0].value,
                                     parent_feeder=worksheet[6][0].value)
                           )
        return results

    def get_inverters(self, dataframe, row_start, row_end):
        results = []
        for col in range(DATA_COLUMN, len(dataframe.columns)):
            worksheet = self.__dataframe_to_worksheet(dataframe=dataframe,
                                                      row_start=row_start,
                                                      row_end=row_end,
                                                      col_start=col,
                                                      col_end=col + 1)
            if self.__is_column_empty(worksheet):
                break
            results.append(InverterDO(name=worksheet[1][0].value,
                                      iec_name=worksheet[2][0].value,
                                      nominal_power_wac=worksheet[3][0].value,
                                      maximum_power_kwac=worksheet[4][0].value,
                                      total_dc_power=worksheet[5][0].value,
                                      states_and_fault_codes=worksheet[6][0].value,
                                      manufacturer=worksheet[7][0].value,
                                      model=worksheet[8][0].value,
                                      firmware_version=worksheet[9][0].value,
                                      dc_input_capacity=worksheet[10][0].value,
                                      number_of_connected_combiners=worksheet[11][0].value,
                                      module_manufacturer=worksheet[12][0].value)
                           )
        return results

    def get_combiners(self, dataframe, row_start, row_end):
        results = []
        for col in range(DATA_COLUMN, len(dataframe.columns)):
            worksheet = self.__dataframe_to_worksheet(dataframe=dataframe,
                                                      row_start=row_start,
                                                      row_end=row_end,
                                                      col_start=col,
                                                      col_end=col + 1)
            if self.__is_column_empty(worksheet):
                break
            results.append(CombinerDO(name=worksheet[1][0].value,
                                      iec_combiner_name=worksheet[2][0].value,
                                      capacity_wcd=worksheet[3][0].value,
                                      manufacturer_and_model=worksheet[4][0].value,
                                      temperature_coefficient=worksheet[5][0].value,
                                      contract_degradation_rate=worksheet[6][0].value,
                                      manufacturer_degradation_rate=worksheet[7][0].value,
                                      measured_degradation_rate=worksheet[8][0].value)
                           )
        return results

    def get_site_level_non_elec(self, dataframe, row_start, row_end):
        results = []
        for col in range(DATA_COLUMN, len(dataframe.columns)):
            worksheet = self.__dataframe_to_worksheet(dataframe=dataframe,
                                                      row_start=row_start,
                                                      row_end=row_end,
                                                      col_start=col,
                                                      col_end=col + 1)
            if self.__is_column_empty(worksheet):
                break
            results.append(SiteLevelNonElecDO(number_of_met_stations=worksheet[1][0].value,
                                              number_of_soiling_stations=worksheet[2][0].value)
                           )
        return results

    def get_met_stations(self, dataframe, row_start, row_end):
        results = []
        for col in range(DATA_COLUMN, len(dataframe.columns)):
            worksheet = self.__dataframe_to_worksheet(dataframe=dataframe,
                                                      row_start=row_start,
                                                      row_end=row_end,
                                                      col_start=col,
                                                      col_end=col + 1)
            if self.__is_column_empty(worksheet):
                break
            results.append(MetStationDO(name=worksheet[1][0].value,
                                        iec_name=worksheet[2][0].value,
                                        number_of_poa_sensors=worksheet[3][0].value,
                                        iec_number_of_poa_sensors=worksheet[4][0].value,
                                        number_of_ghi_sensors=worksheet[5][0].value,
                                        number_of_back_of_module_temperatures=worksheet[6][0].value,
                                        number_of_ambient_temperatures=worksheet[7][0].value)
                           )
        return results

    def get_sensors(self, dataframe, row_start, row_end):
        results = []
        for col in range(DATA_COLUMN, len(dataframe.columns)):
            worksheet = self.__dataframe_to_worksheet(dataframe=dataframe,
                                                      row_start=row_start,
                                                      row_end=row_end,
                                                      col_start=col,
                                                      col_end=col + 1)
            if self.__is_column_empty(worksheet):
                break
            results.append(SensorDO(name=worksheet[1][0].value,
                                    operating_range=worksheet[2][0].value,
                                    manufacturer=worksheet[3][0].value,
                                    model=worksheet[4][0].value,
                                    calibration_date=worksheet[5][0].value,
                                    calibration_value=worksheet[6][0].value,
                                    sensor_type=worksheet[7][0].value)
                           )
        return results

    def get_soiling_stations(self, dataframe, row_start, row_end):
        results = []
        for col in range(DATA_COLUMN, len(dataframe.columns)):
            worksheet = self.__dataframe_to_worksheet(dataframe=dataframe,
                                                      row_start=row_start,
                                                      row_end=row_end,
                                                      col_start=col,
                                                      col_end=col + 1)
            if self.__is_column_empty(worksheet):
                break
            results.append(SoilingStationDO(name=worksheet[1][0].value,
                                            soiling_rate=worksheet[2][0].value,
                                            last_cleaning_date=worksheet[3][0].value,
                                            last_calibration_date=worksheet[4][0].value)
                           )
            return results

    def get_trackers(self, dataframe, row_start, row_end):
        results = []
        for col in range(DATA_COLUMN, len(dataframe.columns)):
            worksheet = self.__dataframe_to_worksheet(dataframe=dataframe,
                                                      row_start=row_start,
                                                      row_end=row_end,
                                                      col_start=col,
                                                      col_end=col + 1)
            if self.__is_column_empty(worksheet):
                break
            results.append(TrackerDO(name=worksheet[1][0].value,
                                     manufacturer=worksheet[2][0].value,
                                     model=worksheet[3][0].value,
                                     axis_orientation=worksheet[4][0].value,
                                     max_rotation_limit_east=worksheet[5][0].value,
                                     max_rotation_limit_west=worksheet[6][0].value,
                                     control_algorithm=worksheet[7][0].value,
                                     modules_on_tracker_row=worksheet[8][0].value,
                                     modules_layout_on_trackers=worksheet[9][0].value,
                                     post_to_post_separation=worksheet[10][0].value,
                                     stow_position_snow=worksheet[11][0].value,
                                     stow_position_wind=worksheet[12][0].value,
                                     block=worksheet[13][0].value,
                                     assoc_electrical_pvps=worksheet[14][0].value,
                                     controller_number=worksheet[15][0].value,
                                     motor_number=worksheet[16][0].value,
                                     row_height=worksheet[17][0].value,
                                     modules_per_row=worksheet[18][0].value,
                                     rows_per_motor=worksheet[19][0].value)
                           )
        return results

    def get_meter_box(self, dataframe, row_start, row_end):
        results = []
        for col in range(DATA_COLUMN, len(dataframe.columns)):
            worksheet = self.__dataframe_to_worksheet(dataframe=dataframe,
                                                      row_start=row_start,
                                                      row_end=row_end,
                                                      col_start=col,
                                                      col_end=col + 1)
            if self.__is_column_empty(worksheet):
                break
            results.append(MeterBoxDO(name=worksheet[1][0].value,
                                      iec_name=worksheet[2][0].value,
                                      deeper_level_asset_ref=worksheet[3][0].value,
                                      meterkind=worksheet[4][0].value)
                           )
            return results

    def __dataframe_to_worksheet(self, col_end, col_start, dataframe, row_end, row_start):
        dataframe = dataframe.iloc[row_start:row_end][list(dataframe.columns[col_start:col_end])]
        worksheet = Workbook().create_sheet()
        for row in dataframe_to_rows(dataframe, index=False, header=False):
            worksheet.append(row)
        return worksheet

    def __is_column_empty(self, worksheet):
        for cell in worksheet.rows:
            if cell[0].value == cell[0].value:
                return False
        return True


if __name__ == '__main__':
    main = Main(SITE_CHAR_FILE)
    main.run()
