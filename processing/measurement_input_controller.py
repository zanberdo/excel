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
from data_objects import TagListDO


class MeasurementInputController:

    def __init__(self) -> None:
        self.columns = ['Applicable to on-boarded site',
                        'AssetType',
                        'measurementType',
                        'business_description',
                        'LN_prefix',
                        'LN_lnClass',
                        'Max LN_inst',
                        'DOName',
                        'DAName',
                        'dataFormat',
                        'name_SIUnit',
                        'MeasurementType',
                        'IEC61850MeasurementReferential-qaqc_sequence',
                        'IEC61850MeasurementReferential-qaqc_priority',
                        'Analog-AnalogLimitSet',
                        'Analog-DataSourceID',
                        'tech_source_measurement_Rel-name_tech_source',
                        'tech_source_measurement_Rel-data_time_zone',
                        'tech_source_measurement_Rel-static_time_offset',
                        'tech_source_measurement_Rel-rdl_connection_date',
                        'tech_source_measurement_Rel-rdl_disconnection_date',
                        'tech_source_measurement_Rel-template_switch_state_mapping',
                        'raw_unit_symbol_automaticallyAvailable',
                        'raw_unitMultiplier_value',
                        'raw_unitSymbol_value']

    def get_measurements_dataframe(self, tag_list_dos: List[TagListDO]) -> DataFrame:
        logger.debug('get_measurements_dataframe([tag_list_dos])')
        rows = []
        for tag_list_do in tag_list_dos:
            applicable_to_onboarded_site = "Yes" if tag_list_do.scada_tag_name != "N/A" else "No"

            pvps_level_mapping = {
                "SITE - HV": "Bay",
                "SITE - MV": "Feeder",
                "CBOX": "CombinerBox_Level_A",
                "FEEDER": "Feeder",
                "INV": "ACDCConverter",
                "MET": "EnvironmentalMonitoringStation",
                "METER": "MeterBox",
                "Tracker": "Tracker",
                "CURTAILMENT": "GeneralSystemOperator"
            }
            asset_type = pvps_level_mapping.get(tag_list_do.pvps_level, None)

            if "mxVal" in tag_list_do.iec61850_logical_node or "stVal" in tag_list_do.iec61850_logical_node:
                measurement_type = "Discrete"
            elif "mag.f" in tag_list_do.iec61850_logical_node:
                if tag_list_do.pvps_level == "MET":
                    measurement_type = "AtmosphericAnalog"
                else:
                    measurement_type = "Analog"
            else:
                logger.warning(f"iec61850_logical_node: {tag_list_do.iec61850_logical_node}")
                raise Exception("invalid measurement type: must contain mxVal/stVal for Discrete or mag.f for Analog")

            if measurement_type == "Discrete":
                business_description = f"Event measurements of {tag_list_do.operational_data}"
                measurement_type_description = f"{asset_type} Event measurements of {tag_list_do.operational_data}"

            ln_prefix = None

            ln_split = tag_list_do.iec61850_logical_node.split("\n")[0].split(".")

            ln_class = re.sub(r'\d+$', '', re.sub(r'\[.*\#\]', '', ln_split[0]))

            max_ln_inst = re.sub(r'^.*\D+', '', re.sub(r'\[.*\#\]', '1', ln_split[0]))

            if tag_list_do.pvps_level == "CBOX":
                max_ln_inst = None
                ln_class = re.sub(r'^In', '', ln_class)

            do_name = re.sub(r'\[.*\#\]', '1', ln_split[1])

            da_name = ".".join(ln_split[2:])
            if da_name == "mxVal.mag.f":
                da_name = "mxVal"

            data_format = tag_list_do.value_type

            name_si_unit = tag_list_do.default_uom

            iec61850_measurement_referential_qaqc_sequence = None
            iec61850_measurement_referential_qaqc_priority = None
            analog_analog_limit_set = None
            analog_data_source_id = "S3"
            tech_source_measurement_rel_name_tech_source = "T4"
            tech_source_measurement_rel_data_time_zone = "UTC"
            tech_source_measurement_rel_static_time_offset = None

            # TODO: ianb - revisit these, should not be hardcoded - 20201208
            tech_source_measurement_rel_rdl_connection_date = "2020-01-01"
            tech_source_measurement_rel_rdl_disconnection_date = None
            tech_source_measurement_rel_template_switch_state_mapping = None

            raw_unit_symbol_automaticallyAvailable = "yes via PI AF File"
            raw_unitMultiplier_value = None
            raw_unitSymbol_value = None

            meas_inputs = []
            if "Analog" in measurement_type:
                s4_iec61850_measurement_referential_qaqc_sequence = \
                    "[uniqueness_microBatch-0.1, (completeness_analog_10min_microBatch-0.1, " \
                    "validity_analog_10min_microBatch-0.1, consistency_analog_10min_microBatch-0.1)]"
                s4_iec61850_measurement_referential_qaqc_priority = "0"
                iec61850_measurement_referential_qaqc_sequence = \
                    "[uniqueness_microBatch-0.1, completeness_analog_10min_microBatch-0.1]"
                iec61850_measurement_referential_qaqc_priority = "1"

                s4_analog_analog_limit_set = f"ALL_GENERIC_{ln_class}.{do_name}.{da_name}"
                if "METEOSTA" in tag_list_do.logical_device:
                    s4_analog_analog_limit_set = f"ALL_MetStation_{ln_class}.{do_name}.{da_name}"
                elif "_SUB0" in tag_list_do.logical_device:
                    s4_analog_analog_limit_set = f"ALL_SubtationLevel_{ln_class}.{do_name}.{da_name}"

                ln_prefixes = [
                    ("s2", "minimum", tag_list_do.min),
                    ("s3", "maximum", tag_list_do.max),
                    ("s4", "average", tag_list_do.average_10min),
                    ("s5", "standard deviation", tag_list_do.population_standard_deviation),
                ]

                for analog_prefix in ln_prefixes:
                    if analog_prefix[2] == "X":
                        ln_prefix = analog_prefix[0]
                        agg_type = analog_prefix[1]

                        business_description = f"10 minute {agg_type} of {tag_list_do.operational_data}"
                        measurement_type_description = \
                            f"{asset_type} 10 minutes {agg_type} of {tag_list_do.operational_data}"

                        if tag_list_do.pvps_level == "CBOX":
                            ln_prefix = f"In_{ln_prefix}"

                        if ln_prefix == "s4":
                            sx_iec61850_measurement_referential_qaqc_sequence = \
                                s4_iec61850_measurement_referential_qaqc_sequence
                            sx_iec61850_measurement_referential_qaqc_priority = \
                                s4_iec61850_measurement_referential_qaqc_priority
                            sx_analog_analog_limit_set = s4_analog_analog_limit_set
                        else:
                            sx_iec61850_measurement_referential_qaqc_sequence = \
                                iec61850_measurement_referential_qaqc_sequence
                            sx_iec61850_measurement_referential_qaqc_priority = \
                                iec61850_measurement_referential_qaqc_priority
                            sx_analog_analog_limit_set = analog_analog_limit_set

                        meas_inputs.append([
                            applicable_to_onboarded_site,
                            asset_type,
                            measurement_type,
                            business_description,
                            ln_prefix,
                            ln_class,
                            max_ln_inst,
                            do_name,
                            da_name,
                            data_format,
                            name_si_unit,
                            measurement_type_description,
                            sx_iec61850_measurement_referential_qaqc_sequence,
                            sx_iec61850_measurement_referential_qaqc_priority,
                            sx_analog_analog_limit_set,
                            analog_data_source_id,
                            tech_source_measurement_rel_name_tech_source,
                            tech_source_measurement_rel_data_time_zone,
                            tech_source_measurement_rel_static_time_offset,
                            tech_source_measurement_rel_rdl_connection_date,
                            tech_source_measurement_rel_rdl_disconnection_date,
                            tech_source_measurement_rel_template_switch_state_mapping,
                            raw_unit_symbol_automaticallyAvailable,
                            raw_unitMultiplier_value,
                            raw_unitSymbol_value
                        ])
            else:
                meas_inputs.append([
                    applicable_to_onboarded_site,
                    asset_type,
                    measurement_type,
                    business_description,
                    ln_prefix,
                    ln_class,
                    max_ln_inst,
                    do_name,
                    da_name,
                    data_format,
                    name_si_unit,
                    measurement_type_description,
                    iec61850_measurement_referential_qaqc_sequence,
                    iec61850_measurement_referential_qaqc_priority,
                    analog_analog_limit_set,
                    analog_data_source_id,
                    tech_source_measurement_rel_name_tech_source,
                    tech_source_measurement_rel_data_time_zone,
                    tech_source_measurement_rel_static_time_offset,
                    tech_source_measurement_rel_rdl_connection_date,
                    tech_source_measurement_rel_rdl_disconnection_date,
                    tech_source_measurement_rel_template_switch_state_mapping,
                    raw_unit_symbol_automaticallyAvailable,
                    raw_unitMultiplier_value,
                    raw_unitSymbol_value
                ])

            rows += meas_inputs

        dataframe = pd.DataFrame(data=rows, columns=self.columns)
        return dataframe
