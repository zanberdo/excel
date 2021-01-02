import logging
import re
from typing import List

import pandas as pd
from pandas import DataFrame

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.debug('Loading MetStationInputController...')

logger.debug('Importing packages from relative path...')
from data_objects import MetStationDO


class MetStationInputController:

    def __init__(self, project_code: str, country: str) -> None:
        self.project_code = project_code
        self.country = country
        self.columns = ['SQL extract',
                        'MetSta number',
                        'LDevice_inst',
                        'Layer_ALL_Contractual',
                        'Layer_ALL_ISOGeographical',
                        'Naming_EnvironmentalMonitoringStation_Contractual',
                        'POASensor_number',
                        'GHISensor_number',
                        'BackOfModuleTempSensor_number',
                        'AmbientTempSensor_number']

    def get_met_station_dataframe(self, met_station_dos: List[MetStationDO]) -> DataFrame:
        logger.debug('get_met_station_dataframe([met_station_dos])')
        rows = []
        for met_station_do in met_station_dos:
            sql_extract = f'{self.project_code}-{met_station_do.name}'
            metsta_number = re.split('-', met_station_do.name)[0][-1].rjust(2, '0')
            ldevice_inst = met_station_do.iec_name
            layer_all_contractual = self.project_code
            layer_all_isogeo = self.country
            naming_env_mon_sta = sql_extract
            poa_sensors = met_station_do.number_of_poa_sensors
            ghi_sensors = met_station_do.number_of_ghi_sensors
            bom_temp_sensors = met_station_do.number_of_bom_temp_sensors
            amb_temp_sensors = met_station_do.number_of_ambient_temp_sensors
            rows.append(
                [sql_extract,
                 metsta_number,
                 ldevice_inst,
                 layer_all_contractual,
                 layer_all_isogeo,
                 naming_env_mon_sta,
                 poa_sensors,
                 ghi_sensors,
                 bom_temp_sensors,
                 amb_temp_sensors])

        dataframe = pd.DataFrame(data=rows, columns=self.columns)
        return dataframe
