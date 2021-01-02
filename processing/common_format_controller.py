import logging
import os
from typing import List

from pandas import DataFrame
from s3fs import S3FileSystem

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.debug('Loading CommonFormatController...')

logger.debug('Importing packages from relative path...')
from utils import Utils
from data_objects import CombinerDO
from data_objects import InverterDO
from data_objects import MetStationDO
from data_objects import MeterBoxDO
from data_objects import ShelterDO
from data_objects import SiteLevelDO
from data_objects import TagListDO
from asset_info_input_controller import AssetInfoInputController
from asset_list_input_controller import AssetListInputController
from electrical_input_controller import ElectricalInputController
from location_input_controller import LocationInputController
from measurement_input_controller import MeasurementInputController
from met_station_input_controller import MetStationInputController
from meter_box_input_controller import MeterBoxInputController


class CommonFormatController:

    def __init__(self, project_code: str, file_system: S3FileSystem()):
        self.fs = file_system
        self.project_code = project_code
        self.utils = Utils()

    def write_met_station_input(self, site_level_dos: List[SiteLevelDO],
                                met_station_dos: List[MetStationDO]) -> None:
        logger.info('Processing MetStaInput.csv...')
        project_code = site_level_dos[0].project_code
        country = site_level_dos[0].country
        controller = MetStationInputController(project_code=project_code, country=country)
        dataframe = controller.get_met_station_dataframe(met_station_dos=met_station_dos)
        logger.info('Writing MetStaInput.csv...')
        self.__write_common_file(dataframe=dataframe, filename='MetStaInput.csv')

    def write_location_input(self, site_level_dos: List[SiteLevelDO]) -> None:
        logger.info('Processing LocationInput.csv...')
        controller = LocationInputController()
        dataframe = controller.get_location_dataframe(site_level_dos=site_level_dos)
        logger.info('Writing LocationInput.csv...')
        self.__write_common_file(dataframe=dataframe, filename='LocationInput.csv')

    def write_electrical_input(self, site_level_dos: List[SiteLevelDO],
                               combiner_dos: List[CombinerDO],
                               inverter_dos: List[InverterDO],
                               shelter_dos: List[ShelterDO]) -> None:
        logger.info('Processing CommonFormat-ElectricalInput.csv...')
        project_code = site_level_dos[0].project_code
        country = site_level_dos[0].country
        cod = site_level_dos[0].cod
        controller = ElectricalInputController(project_code=project_code, country=country, cod=cod)
        dataframe = controller.get_electrical_dataframe(combiner_dos=combiner_dos, inverter_dos=inverter_dos,
                                                        shelter_dos=shelter_dos)
        logger.info('Writing CommonFormat-ElectricalInput.csv...')
        self.__write_common_file(dataframe=dataframe, filename='CommonFormat-ElectricalInput.csv')

    def write_meter_box_input(self, site_level_dos: List[SiteLevelDO],
                              meter_box_dos: List[MeterBoxDO]) -> None:
        logger.info('Processing MeterInput.csv...')
        project_code = site_level_dos[0].project_code
        country = site_level_dos[0].country
        controller = MeterBoxInputController(project_code=project_code, country=country)
        dataframe = controller.get_meter_box_dataframe(meter_box_dos=meter_box_dos)
        logger.info('Writing MeterInput.csv...')
        self.__write_common_file(dataframe=dataframe, filename='MeterInput.csv')

    def write_meas_input(self, tag_list_dos: List[TagListDO]) -> None:
        logger.info('Processing MeasInput.csv...')
        controller = MeasurementInputController()
        dataframe = controller.get_measurements_dataframe(tag_list_dos=tag_list_dos)
        logger.info('Writing MeasInput.csv...')
        self.__write_common_file(dataframe=dataframe, filename='MeasInput.csv')

    def write_asset_list_input(self, combiner_dos: List[CombinerDO]) -> None:
        logger.info('Processing AssetListInput.csv...')
        controller = AssetListInputController()
        dataframe = controller.get_asset_list_dataframe(combiner_dos=combiner_dos)
        logger.info('Writing AssetListInput.csv...')
        self.__write_common_file(dataframe=dataframe, filename='AssetListInput.csv')

    def write_asset_info_input(self, inverter_dos: List[InverterDO], combiner_dos: List[CombinerDO]) -> None:
        logger.info('Processing AssetInfoInput.csv...')
        controller = AssetInfoInputController()
        dataframe = controller.get_asset_info_dataframe(combiner_dos=combiner_dos, inverter_dos=inverter_dos)
        logger.info('Writing AssetInfoInput.csv...')
        self.__write_common_file(dataframe=dataframe, filename='AssetInfoInput.csv')

    def __write_common_file(self, dataframe: DataFrame, filename: str) -> None:
        logger.debug(f'dataframe:\n{dataframe.to_string()}')
        common_file = f'{os.environ["S3_BUCKET_COMMON"]}/{self.project_code}/{filename}'
        logger.debug(f'Processing {common_file}...')
        with self.fs.open(path=common_file, mode="w", newline="") as file:
            dataframe.to_csv(path_or_buf=file, index=False)
