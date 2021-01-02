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
from data_objects import CombinerDO
from data_objects import InverterDO


class AssetInfoInputController:

    def __init__(self) -> None:
        self.columns = [
            'modelNumber',
            'modelVersion',
            'description',
            'name',
            'catalogueNumber',
            'instructionManual',
            'UmppMin_value',
            'UmppMax_value',
            'DCMaxVoltage_value',
            'DCMaxCurrent_value',
            'DCMaxPower_value',
            'DCNameplate_value',
            'tempCoeffNameplate_value',
            'DCPeakPower_value',
            'ACMaxPower_value',
            'ACNameplate_value',
            'manufacturer',
            'EventList_name'
        ]
        self.manufacturer_trigram = {
            'Canadian Solar': 'CSI',
            'Trina': 'TSL',
            'Power Electronics': 'PES',
            'Xantrex': 'XTX',
            'First Solar': 'FSL',
            'Solar Frontier': 'SFK'
        }

    def get_asset_info_dataframe(self, combiner_dos: List[CombinerDO], inverter_dos: List[InverterDO]) -> DataFrame:
        logger.debug('get_asset_info_dataframe([combiner_dos], [inverter_dos], [shelter_dos])')
        unique_inverter_dos = {}
        for inverter_do in inverter_dos:
            inverter_do_unique_hash = inverter_do.get_unique_hash()
            if inverter_do_unique_hash not in unique_inverter_dos.keys():
                unique_inverter_dos[inverter_do_unique_hash] = inverter_do

        rows = []
        for inverter_do in unique_inverter_dos.values():
            model_number = inverter_do.model if inverter_do.model else 'NULL'
            model_version = '' if pd.isna(inverter_do.firmware_version) else inverter_do.firmware_version
            description = f'Manufacturer reference for {inverter_do.manufacturer} {inverter_do.model} ' \
                          f'{model_version}'.rstrip()
            name = f'inverter_{inverter_do.model.replace(" ", "")}'
            catalogue_number = 'NULL'
            instruction_manual = 'NULL'
            umpp_min = 'NULL'
            umpp_max = 'NULL'
            dc_max_voltage = 'NULL'
            dc_max_current = 'NULL'
            dc_max_power = 'NULL'
            dc_nameplate = 'NULL'
            temp_coefficient_nameplate = 'NULL'
            dc_peak_power = 'NULL'
            # Required field
            # ac_max_power = inverter_do.maximum_power_kwac
            ac_max_power = 'NULL' if pd.isna(inverter_do.maximum_power_kwac) else inverter_do.maximum_power_kwac
            ac_nameplate = inverter_do.nominal_power_wac
            manufacturer = inverter_do.manufacturer
            eventlist_name = inverter_do.eventlist_name
            rows.append([
                model_number,
                model_version,
                description,
                name,
                catalogue_number,
                instruction_manual,
                umpp_min,
                umpp_max,
                dc_max_voltage,
                dc_max_current,
                dc_max_power,
                dc_nameplate,
                temp_coefficient_nameplate,
                dc_peak_power,
                ac_max_power,
                ac_nameplate,
                manufacturer,
                eventlist_name
            ])

        for combiner_do in combiner_dos:
            model_number = f'cbox_{combiner_do.model} {combiner_do.iec_name}'
            model_version = 'NULL'
            description = f'CIM_Extension CombinerBox electrically linked to {combiner_do.manufacturer} ' \
                          f'{combiner_do.model}'
            name = f'combinerBox_{combiner_do.iec_name}'
            catalogue_number = 'NULL'
            instruction_manual = 'NULL'
            umpp_min = 'NULL'
            umpp_max = 'NULL'
            dc_max_voltage = 'NULL'
            dc_max_current = 'NULL'
            dc_max_power = 'NULL'
            dc_nameplate = 'NULL'
            temp_coefficient_nameplate = combiner_do.temperature_coefficient
            dc_peak_power = combiner_do.capacity_wdc
            ac_max_power = 'NULL'
            ac_nameplate = 'NULL'
            manufacturer = self.manufacturer_trigram[combiner_do.manufacturer]
            eventlist_name = 'NULL'
            rows.append([
                model_number,
                model_version,
                description,
                name,
                catalogue_number,
                instruction_manual,
                umpp_min,
                umpp_max,
                dc_max_voltage,
                dc_max_current,
                dc_max_power,
                dc_nameplate,
                temp_coefficient_nameplate,
                dc_peak_power,
                ac_max_power,
                ac_nameplate,
                manufacturer,
                eventlist_name
            ])

        dataframe = pd.DataFrame(data=rows, columns=self.columns)
        return dataframe
