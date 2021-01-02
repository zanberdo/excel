import logging
import re
from datetime import datetime
from typing import List

import pandas as pd
from pandas import DataFrame

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.debug('Loading ElectricalInputController...')

logger.debug('Importing packages from relative path...')
from data_objects import CombinerDO
from data_objects import InverterDO
from data_objects import ShelterDO


class ElectricalInputController:

    def __init__(self, project_code: str, country: str, cod: datetime) -> None:
        self.project_code = project_code
        self.country = country
        self.cod = cod
        self.columns = [
            'Asset Ref Code',
            'SHELTER SQL',
            'INVERTER SQL',
            'Cbox level B SQL',
            'PARC SQL',
            'Parc Basic Ref',
            'Bay - AC',
            'Feeder - AC',
            'InverterStation - AC',
            'ACDCConverter - AC/DC',
            'CombinerBox A - DC',
            'Dcbusbar A - DC',
            'CombinerBox B - DC',
            'Dcbusbar B - DC',
            'Layer_ALL_Contractual',
            'Layer_ALL_ISOGeographical',
            'Name_InverterStation_Contractual',
            'Name_ACDCConverter_Contractual',
            'Name_CombinerBoxB_Contractual',
            'Asset_ALL_InUseDate',
            'PAM_CombinerBoxB_DCPeakPower',
            'PAM_CombinerBoxB_tempCoeffNemplate_value',
            'PAM_InverterRef'
        ]

    def get_electrical_dataframe(self, combiner_dos: List[CombinerDO],
                                 inverter_dos: List[InverterDO],
                                 shelter_dos: List[ShelterDO]) -> DataFrame:
        logger.debug('get_electrical_dataframe([combiner_dos], [inverter_dos], [shelter_dos])')
        # TODO: Accept 'COD' as 'TBD' and log when this happens - Aamir will talk to Peter and
        #       Addy about appropriate values
        python_date = f'{self.cod.year}-{self.cod.month:02d}-{self.cod.day:02d}'
        rows = []
        for combiner_do in combiner_dos:
            asset_ref_code = f'{self.project_code}-{re.split("-", combiner_do.name)[0]}-' \
                             f'{re.split("-", combiner_do.name)[1]}-S{re.split("-", combiner_do.name)[2]}'
            shelter_sql = f'{self.project_code}-{re.split("-", combiner_do.name)[0]}'
            inverter_sql = f'{shelter_sql}-{re.split("-", combiner_do.name)[1]}'
            cbox_level_b_sql = f'{inverter_sql}-{re.split("-", combiner_do.name)[2]}'
            parc_sql = self.project_code
            parc_basic_ref = "_".join(re.split("_", combiner_do.iec_name)[:3])
            bay = f'{parc_basic_ref}_SUB001LevHv01Upgrid01Cell'
            shelter_iec_name = '_'.join(re.split("_", combiner_do.iec_name)[:4])
            shelter_do = next((found for found in shelter_dos if found.iec_name == shelter_iec_name), None)
            if shelter_do is None:
                logger.error(
                    f"While processing Combiner IEC 61850: '{combiner_do.iec_name}' "
                    f"Failed to find Shelter IEC 61850: '{shelter_iec_name}' "
                    f"in shelters: {[shelter_do.iec_name for shelter_do in shelter_dos]}.")
                raise Exception(f"Failed to find Shelter '{shelter_iec_name}' for Combiner '{combiner_do.iec_name}'")

            feeder = shelter_do.parent_feeder
            inverter_station = '_'.join(re.split('_', combiner_do.iec_name)[:4])
            inverter_iec_name = f'{shelter_iec_name}Inverter{(re.split("_", combiner_do.iec_name)[4])[-2:]}'
            inverter_do = next((found for found in inverter_dos if found.iec_name == inverter_iec_name), None)
            if inverter_do is None:
                logger.error(
                    f"While processing Combiner IEC 61850: '{combiner_do.iec_name}' "
                    f"Failed to find Inverter IEC 61850: '{inverter_iec_name}' "
                    f"in inverters: {[inverter_do.iec_name for inverter_do in inverter_dos]}."
                )
                raise Exception(f"Failed to find Inverter '{inverter_iec_name}' for Combiner '{combiner_do.iec_name}'")
            acdc_converter = None if inverter_do is None else inverter_do.iec_name

            combiner_a = "_".join(re.split("_", combiner_do.iec_name)[:5])
            dcbusbar_a = f'{combiner_a}_BBS000001'
            combiner_b = combiner_do.iec_name
            dcbusbar_b = f'{combiner_do.iec_name}_BBS000001'
            layer_all_contractual = self.project_code
            layer_all_iso_geographical = self.country
            name_inverter_station_contractual = shelter_sql
            name_acdc_converter_contractual = inverter_sql
            name_combiner_b_contractual = f'{inverter_sql}-S{re.split("-", combiner_do.name)[2]}'
            asset_all_in_use_date = python_date
            pam_combiner_b_dc_peak_power = combiner_do.capacity_wdc / 1_000_000
            pam_combiner_b_temp_coefficient = combiner_do.temperature_coefficient
            pam_inverter_ref = f'{inverter_do.manufacturer}_{inverter_do.model}'
            rows.append(
                [asset_ref_code,
                 shelter_sql,
                 inverter_sql,
                 cbox_level_b_sql,
                 parc_sql,
                 parc_basic_ref,
                 bay,
                 feeder,
                 inverter_station,
                 acdc_converter,
                 combiner_a,
                 dcbusbar_a,
                 combiner_b,
                 dcbusbar_b,
                 layer_all_contractual,
                 layer_all_iso_geographical,
                 name_inverter_station_contractual,
                 name_acdc_converter_contractual,
                 name_combiner_b_contractual,
                 asset_all_in_use_date,
                 pam_combiner_b_dc_peak_power,
                 pam_combiner_b_temp_coefficient,
                 pam_inverter_ref])

        dataframe = pd.DataFrame(data=rows, columns=self.columns)
        return dataframe
