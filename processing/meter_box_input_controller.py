import logging
from typing import List

import pandas as pd
from pandas import DataFrame

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.debug('Loading MeterBoxInputController...')

logger.debug('Importing packages from relative path...')
from data_objects import MeterBoxDO


class MeterBoxInputController:

    def __init__(self, project_code: str, country: str) -> None:
        self.project_code = project_code
        self.country = country
        self.columns = [
            'MeterReference',
            'Deeper level asset reference',
            'MeterKind',
            'Layer_ALL_Contractual',
            'Layer_ALL_ISOGeographical',
            'Naming_InverterStation_Contractual'
        ]

    def get_meter_box_dataframe(self, meter_box_dos: List[MeterBoxDO]) -> DataFrame:
        logger.debug('get_meter_box_dataframe([meter_box_dos])')
        rows = []
        for meter_box_do in meter_box_dos:
            meter_reference = meter_box_do.iec_name
            asset_reference = meter_box_do.deeper_level_asset_ref
            meterkind = meter_box_do.meterkind
            layer_all_contractual = self.project_code
            layer_all_iso_geographical = self.country
            name_inverter_station_contractual = 'NULL'
            rows.append(
                [meter_reference,
                 asset_reference,
                 meterkind,
                 layer_all_contractual,
                 layer_all_iso_geographical,
                 name_inverter_station_contractual])
        dataframe = pd.DataFrame(data=rows, columns=self.columns)
        return dataframe
