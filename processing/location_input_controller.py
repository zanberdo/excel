import logging
from typing import List

import pandas as pd
from pandas import DataFrame

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.debug('Loading LocationInputController...')

logger.debug('Importing packages from relative path...')
from utils import Utils
from data_objects import SiteLevelDO


class LocationInputController:

    def __init__(self) -> None:
        self.columns = [
            'Location-type',
            'Location-Name',
            'Location-description',
            'crsUrn_CS',
            'xPosition',
            'yPosition',
            'zPosition',
            'Layer-Name',
            'name_StreetAddress',
            'projectCode',
            'geoInfoReference'
        ]

    def get_location_dataframe(self, site_level_dos: List[SiteLevelDO]) -> DataFrame:
        logger.debug('get_location_dataframe([site_level_dos])')
        utils = Utils()
        site_project_code = site_level_dos[0].project_code
        rows = []
        for site_level_do in site_level_dos:
            location_type = 'ContractualInfo'
            location_name = f'ContractualProject{site_project_code}'
            location_description = f'Location defining the coordinate system for {site_project_code}, ' \
                                   f'based on average inverter location'
            crsurn_cd = 'urn:ogc:dev:crs:EPSG::4326'
            xposition = utils.parse_dms(site_level_do.longitude)
            yposition = utils.parse_dms(site_level_do.latitude)
            zposition = 'NULL'  # TODO: Calculate based on lat/long
            layer_name = f'{site_project_code}'
            name_street_address = 'NULL'
            project_code = 'NULL'
            geo_info_reference = 'NULL'
            rows.append(
                [location_type,
                 location_name,
                 location_description,
                 crsurn_cd,
                 xposition,
                 yposition,
                 zposition,
                 layer_name,
                 name_street_address,
                 project_code,
                 geo_info_reference])

        dataframe = pd.DataFrame(data=rows, columns=self.columns)
        return dataframe
