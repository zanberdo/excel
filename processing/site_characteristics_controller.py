import logging
from typing import List

from pandas.core.frame import DataFrame

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.debug('Loading SiteCharacteristicsController...')

logger.debug('Importing packages from relative path...')
from utils import Utils
from data_objects import CombinerDO
from data_objects import FeederDO
from data_objects import InverterDO
from data_objects import MetStationDO
from data_objects import MeterBoxDO
from data_objects import SensorDO
from data_objects import ShelterDO
from data_objects import SiteLevelDO
from data_objects import SiteLevelNonElecDO
from data_objects import SoilingStationDO
from data_objects import TrackerDO


class SiteCharacteristicsController:

    def __init__(self, data_column_offset: int) -> None:
        self.utils = Utils()
        self.data_column_offset = data_column_offset

    def get_site_level(self, dataframe: DataFrame, row_offset: int, rows: int) -> List[SiteLevelDO]:
        logger.info('Getting Site Level data objects...')
        if not isinstance(dataframe, DataFrame):
            raise Exception(f'Parameter {dataframe}({type(dataframe)}) is not a DataFrame')
        section_dataframe = dataframe.iloc[row_offset:row_offset + rows]
        assets_dataframe = self.__get_assets_dataframe(dataframe=section_dataframe)
        results = []
        for col in range(len(assets_dataframe.columns)):
            results.append(
                SiteLevelDO(
                    project_code=assets_dataframe.iat[0, col],
                    iec_name=assets_dataframe.iat[1, col],
                    latitude=assets_dataframe.iat[2, col],
                    longitude=assets_dataframe.iat[3, col],
                    module_tilt=assets_dataframe.iat[4, col],
                    module_orientation=assets_dataframe.iat[5, col],
                    capacity_limit_wac=assets_dataframe.iat[6, col],
                    total_capacity_wdc=assets_dataframe.iat[7, col],
                    number_of_feeders=assets_dataframe.iat[8, col],
                    cod=assets_dataframe.iat[9, col])
            )
        return results

    def get_feeders(self, dataframe: DataFrame, row_offset: int, rows: int) -> List[FeederDO]:
        logger.info('Getting Feeder data objects...')
        if not isinstance(dataframe, DataFrame):
            raise Exception(f'Parameter {dataframe}({type(dataframe)}) is not a DataFrame')
        section_dataframe = dataframe.iloc[row_offset:row_offset + rows]
        assets_dataframe = self.__get_assets_dataframe(dataframe=section_dataframe)
        logger.debug(f'\n{assets_dataframe.to_string()}')
        results = []
        for col in range(len(assets_dataframe.columns)):
            results.append(
                FeederDO(
                    name=assets_dataframe.iat[0, col],
                    iec_name=assets_dataframe.iat[1, col],
                    capacity_wac=assets_dataframe.iat[2, col],
                    capacity_wdc=assets_dataframe.iat[3, col],
                    number_of_shelters_inverters=assets_dataframe.iat[4, col],
                    cod=assets_dataframe.iat[5, col],
                    contract_project_code=assets_dataframe.iat[6, col]
                )
            )
        return results

    def get_shelters(self, dataframe: DataFrame, row_offset: int, rows: int) -> List[ShelterDO]:
        logger.info('Getting Shelter data objects...')
        if not isinstance(dataframe, DataFrame):
            raise Exception(f'Parameter {dataframe}({type(dataframe)}) is not a DataFrame')
        section_dataframe = dataframe.iloc[row_offset:row_offset + rows]
        assets_dataframe = self.__get_assets_dataframe(dataframe=section_dataframe)
        logger.debug(f'\n{assets_dataframe.to_string()}')
        results = []
        for col in range(len(assets_dataframe.columns)):
            results.append(
                ShelterDO(
                    name=assets_dataframe.iat[0, col],
                    iec_name=assets_dataframe.iat[1, col],
                    capacity_wac=assets_dataframe.iat[2, col],
                    capacity_wdc=assets_dataframe.iat[3, col],
                    number_of_inverters_per_shelter=assets_dataframe.iat[4, col],
                    parent_feeder=assets_dataframe.iat[5, col]
                )
            )
        return results

    def get_inverters(self, dataframe: DataFrame, row_offset: int, rows: int) -> List[InverterDO]:
        logger.info('Getting Inverter data objects...')
        if not isinstance(dataframe, DataFrame):
            raise Exception(f'Parameter {dataframe}({type(dataframe)}) is not a DataFrame')
        section_dataframe = dataframe.iloc[row_offset:row_offset + rows]
        assets_dataframe = self.__get_assets_dataframe(dataframe=section_dataframe)
        logger.debug(f'\n{assets_dataframe.to_string()}')
        results = []
        for col in range(len(assets_dataframe.columns)):
            results.append(
                InverterDO(
                    name=assets_dataframe.iat[0, col],
                    iec_name=assets_dataframe.iat[1, col],
                    nominal_power_wac=assets_dataframe.iat[2, col],
                    maximum_power_kwac=assets_dataframe.iat[3, col],
                    total_dc_power=assets_dataframe.iat[4, col],
                    states_and_fault_codes=assets_dataframe.iat[5, col],
                    manufacturer=assets_dataframe.iat[6, col],
                    model=assets_dataframe.iat[7, col],
                    eventlist_name=assets_dataframe.iat[8, col],
                    umpp_min=assets_dataframe.iat[9, col],
                    umpp_max=assets_dataframe.iat[10, col],
                    dc_max_voltage=assets_dataframe.iat[11, col],
                    dc_max_current=assets_dataframe.iat[12, col],
                    dc_max_power=assets_dataframe.iat[13, col],
                    dc_nameplate=assets_dataframe.iat[14, col],
                    dc_peak_power=assets_dataframe.iat[15, col],
                    firmware_version=assets_dataframe.iat[16, col],
                    dc_input_capacity=assets_dataframe.iat[17, col],
                    number_of_connected_combiners=assets_dataframe.iat[18, col],
                    module_manufacturer=assets_dataframe.iat[19, col]
                )
            )
        return results

    def get_combiners(self, dataframe: DataFrame, row_offset: int, rows: int) -> List[CombinerDO]:
        logger.info('Getting Combiner data objects...')
        if not isinstance(dataframe, DataFrame):
            raise Exception(f'Parameter {dataframe}({type(dataframe)}) is not a DataFrame')
        section_dataframe = dataframe.iloc[row_offset:row_offset + rows]
        assets_dataframe = self.__get_assets_dataframe(dataframe=section_dataframe)
        logger.debug(f'\n{assets_dataframe.to_string()}')
        results = []
        for col in range(len(assets_dataframe.columns)):
            results.append(
                CombinerDO(
                    name=assets_dataframe.iat[0, col],
                    iec_name=assets_dataframe.iat[1, col],
                    capacity_wdc=assets_dataframe.iat[2, col],
                    manufacturer=assets_dataframe.iat[3, col],
                    model=assets_dataframe.iat[4, col],
                    temperature_coefficient=assets_dataframe.iat[5, col],
                    contract_degradation_rate=assets_dataframe.iat[6, col],
                    manufacturer_degradation_rate=assets_dataframe.iat[7, col],
                    measured_degradation_rate=assets_dataframe.iat[8, col]
                )
            )
        return results

    def get_site_level_non_elec(self, dataframe: DataFrame, row_offset: int, rows: int) -> List[SiteLevelNonElecDO]:
        logger.info('Getting Site Level (non-electrical) data objects...')
        if not isinstance(dataframe, DataFrame):
            raise Exception(f'Parameter {dataframe}({type(dataframe)}) is not a DataFrame')
        section_dataframe = dataframe.iloc[row_offset:row_offset + rows]
        assets_dataframe = self.__get_assets_dataframe(dataframe=section_dataframe)
        logger.debug(f'\n{assets_dataframe.to_string()}')
        results = []
        for col in range(len(assets_dataframe.columns)):
            results.append(
                SiteLevelNonElecDO(
                    number_of_met_stations=assets_dataframe.iat[0, col],
                    number_of_soiling_stations=assets_dataframe.iat[1, col],
                )
            )
        return results

    def get_met_stations(self, dataframe: DataFrame, row_offset: int, rows: int) -> List[MetStationDO]:
        logger.info('Getting Met Station data objects...')
        if not isinstance(dataframe, DataFrame):
            raise Exception(f'Parameter {dataframe}({type(dataframe)}) is not a DataFrame')
        section_dataframe = dataframe.iloc[row_offset:row_offset + rows]
        assets_dataframe = self.__get_assets_dataframe(dataframe=section_dataframe)
        logger.debug(f'\n{assets_dataframe.to_string()}')
        results = []
        for col in range(len(assets_dataframe.columns)):
            results.append(
                MetStationDO(
                    name=assets_dataframe.iat[0, col],
                    iec_name=assets_dataframe.iat[1, col],
                    number_of_poa_sensors=assets_dataframe.iat[2, col],
                    iec_pos_sensors=assets_dataframe.iat[3, col],
                    number_of_rear_facing_sensors=assets_dataframe.iat[4, col],
                    number_of_irradiance_sensors=assets_dataframe.iat[5, col],
                    number_of_ghi_sensors=assets_dataframe.iat[6, col],
                    number_of_bom_temp_sensors=assets_dataframe.iat[7, col],
                    iec_bom_temperature_sensors=assets_dataframe.iat[8, col],
                    number_of_ambient_temp_sensors=assets_dataframe.iat[9, col]
                )
            )
        return results

    def get_sensors(self, dataframe: DataFrame, row_offset: int, rows: int) -> List[SensorDO]:
        logger.info('Getting Sensor data objects...')
        if not isinstance(dataframe, DataFrame):
            raise Exception(f'Parameter {dataframe}({type(dataframe)}) is not a DataFrame')
        section_dataframe = dataframe.iloc[row_offset:row_offset + rows]
        assets_dataframe = self.__get_assets_dataframe(dataframe=section_dataframe)
        logger.debug(f'\n{assets_dataframe.to_string()}')
        results = []
        for col in range(len(assets_dataframe.columns)):
            results.append(
                SensorDO(
                    name=assets_dataframe.iat[0, col],
                    operating_range=assets_dataframe.iat[1, col],
                    manufacturer=assets_dataframe.iat[2, col],
                    model=assets_dataframe.iat[3, col],
                    calibration_date=assets_dataframe.iat[4, col],
                    calibration_value=assets_dataframe.iat[5, col],
                    sensor_type=assets_dataframe.iat[6, col]
                )
            )
        return results

    def get_soiling_stations(self, dataframe: DataFrame, row_offset: int, rows: int) -> List[SoilingStationDO]:
        logger.info('Getting Soiling Station data objects...')
        if not isinstance(dataframe, DataFrame):
            raise Exception(f'Parameter {dataframe}({type(dataframe)}) is not a DataFrame')
        section_dataframe = dataframe.iloc[row_offset:row_offset + rows]
        assets_dataframe = self.__get_assets_dataframe(dataframe=section_dataframe)
        logger.debug(f'\n{assets_dataframe.to_string()}')
        results = []
        for col in range(len(assets_dataframe.columns)):
            results.append(
                SoilingStationDO(
                    name=assets_dataframe.iat[0, col],
                    soiling_rate=assets_dataframe.iat[1, col],
                    last_cleaning_date=assets_dataframe.iat[2, col],
                    last_calibration_date=assets_dataframe.iat[3, col]
                )
            )
        return results

    def get_trackers(self, dataframe: DataFrame, row_offset: int, rows: int) -> List[TrackerDO]:
        logger.info('Getting Tracker data objects...')
        if not isinstance(dataframe, DataFrame):
            raise Exception(f'Parameter {dataframe}({type(dataframe)}) is not a DataFrame')
        section_dataframe = dataframe.iloc[row_offset:row_offset + rows]
        assets_dataframe = self.__get_assets_dataframe(dataframe=section_dataframe)
        logger.debug(f'\n{assets_dataframe.to_string()}')
        results = []
        for col in range(len(assets_dataframe.columns)):
            results.append(
                TrackerDO(
                    name=assets_dataframe.iat[0, col],
                    manufacturer=assets_dataframe.iat[1, col],
                    model=assets_dataframe.iat[2, col],
                    axis_orientation=assets_dataframe.iat[3, col],
                    max_rotation_limit_east=assets_dataframe.iat[4, col],
                    max_rotation_limit_west=assets_dataframe.iat[5, col],
                    control_algorithm=assets_dataframe.iat[6, col],
                    modules_on_tracker_row=assets_dataframe.iat[7, col],
                    modules_layout_on_trackers=assets_dataframe.iat[8, col],
                    post_to_post_separation=assets_dataframe.iat[9, col],
                    stow_position_snow=assets_dataframe.iat[10, col],
                    stow_position_wind=assets_dataframe.iat[11, col],
                    block=assets_dataframe.iat[12, col],
                    assoc_electrical_pvps=assets_dataframe.iat[13, col],
                    controller_number=assets_dataframe.iat[14, col],
                    motor_number=assets_dataframe.iat[15, col],
                    row_height=assets_dataframe.iat[16, col],
                    modules_per_row=assets_dataframe.iat[17, col],
                    rows_per_motor=assets_dataframe.iat[18, col]
                )
            )
        return results

    def get_meter_box(self, dataframe: DataFrame, row_offset: int, rows: int) -> List[MeterBoxDO]:
        logger.info('Getting Meter Box data objects...')
        if not isinstance(dataframe, DataFrame):
            raise Exception(f'Parameter {dataframe}({type(dataframe)}) is not a DataFrame')
        section_dataframe = dataframe.iloc[row_offset:row_offset + rows]
        logger.debug(f'\n{section_dataframe.to_string()}')
        assets_dataframe = self.__get_assets_dataframe(dataframe=section_dataframe)
        logger.debug(f'\n{assets_dataframe.to_string()}')
        results = []
        for col in range(len(assets_dataframe.columns)):
            results.append(
                MeterBoxDO(
                    name=assets_dataframe.iat[0, col],
                    iec_name=assets_dataframe.iat[1, col],
                    deeper_level_asset_ref=assets_dataframe.iat[2, col],
                    meterkind=assets_dataframe.iat[3, col]
                )
            )
            return results

    def __get_assets_dataframe(self, dataframe):
        df = dataframe.iloc[:][list(dataframe.columns[self.data_column_offset:])]
        empty_column_list = df.columns[df.isna().all()].values
        empty_column_offset = empty_column_list[0] if len(empty_column_list) else len(dataframe.columns)
        section_dataframe = dataframe.iloc[:][list(dataframe.columns[self.data_column_offset: empty_column_offset])]
        section_dataframe.reset_index(drop=True, inplace=True)
        return section_dataframe
