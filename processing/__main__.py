import logging
import os

import pandas as pd
import s3fs

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info('Loading handler function...')
real_path = os.path.dirname(os.path.realpath(__file__))
logger.info(f'\treal path: {real_path}')

logger.debug('Importing packages from relative path...')
from site_characteristics_controller import SiteCharacteristicsController
from common_format_controller import CommonFormatController
from tag_list_controller import TagListController

S3_GLOBAL_CHECKLIST_FILE = "global checklist for solar site onboarding"
DEFAULT_DATA_COLUMN_OFFSET = 3


def handler(event, context):
    project_code = event.get('projectCode')
    if project_code is None:
        raise Exception(
            'Failed to read "projectCode" from environment variable. Be sure projectCode is provided via event object.'
        )
    data_column_offset = event.get('dataColumnOffset')
    if data_column_offset is None:
        logger.error('Failed to provide "dataColumnOffset" from environment variable. Using default value: 3')
        data_column_offset = DEFAULT_DATA_COLUMN_OFFSET
    s3_global_checklist = f'{os.environ["S3_BUCKET_INPUTS"]}/' \
                          f'{project_code}/' \
                          f'{S3_GLOBAL_CHECKLIST_FILE}_{project_code}.xlsx'
    site_characteristic = "Site characteristic"
    tag_list_requirements = "Tag list requirements"

    # TODO: clean this up! Is missing columns or other validation
    fs = s3fs.S3FileSystem()
    if not fs.exists(s3_global_checklist):
        logger.error(f'File does not exist: {s3_global_checklist}')
        raise FileExistsError(f'Failed to open {s3_global_checklist}')

    logger.info(f'Reading {s3_global_checklist}...')
    with fs.open(path=s3_global_checklist, mode="rb") as file:
        global_checklist_file = file.read()

    workbook = pd.ExcelFile(global_checklist_file)
    site_char_worksheet = [name for name in [x for x in workbook.sheet_names] if
                           site_characteristic.upper() in name.upper()]
    if site_char_worksheet[0] in workbook.sheet_names:
        logger.info(f'Reading {site_char_worksheet}...')
        site_char_controller = SiteCharacteristicsController(data_column_offset=data_column_offset)
        site_characteristics = workbook.parse(sheet_name=site_char_worksheet[0], header=None)

        site_level_dos = site_char_controller.get_site_level(site_characteristics, row_offset=4, rows=10)
        # feeder_dos = site_char_controller.get_feeders(site_characteristics, row_offset=15, rows=7)
        shelter_dos = site_char_controller.get_shelters(site_characteristics, row_offset=23, rows=6)
        inverter_dos = site_char_controller.get_inverters(site_characteristics, row_offset=30, rows=20)
        combiner_dos = site_char_controller.get_combiners(site_characteristics, row_offset=51, rows=9)
        # site_level_non_elec_dos = site_char_controller.get_site_level_non_elec(site_characteristics,
        #                                                                        row_offset=67, rows=2)
        met_station_dos = site_char_controller.get_met_stations(site_characteristics, row_offset=70, rows=10)
        # sensor_dos = site_char_controller.get_sensors(site_characteristics, row_offset=81, rows=7)
        # soiling_station_dos = site_char_controller.get_soiling_stations(site_characteristics, row_offset=89, rows=4)
        # tracker_dos = site_char_controller.get_trackers(site_characteristics, row_offset=94, rows=18)
        meter_box_dos = site_char_controller.get_meter_box(site_characteristics, row_offset=114, rows=4)
    else:
        raise (Exception(f"Failed to find worksheet: [{site_char_worksheet[0]}] in workbook. "
                         f"Worksheets: {workbook.sheet_names}"))

    tag_list_worksheet = [name for name in [x for x in workbook.sheet_names] if
                          tag_list_requirements.upper() in name.upper()]
    if tag_list_worksheet[0] in workbook.sheet_names:
        logger.info(f'Reading {tag_list_worksheet}...')
        tag_list_controller = TagListController()
        tag_list = workbook.parse(sheet_name=tag_list_worksheet[0], header=None)

        tag_list_dos = tag_list_controller.get_tag_list(tag_list, row_start=19, rows=33)
    else:
        raise (Exception(f"Failed to find worksheet: [{site_char_worksheet[0]}] in workbook. "
                         f"Worksheets: {workbook.sheet_names}"))

    controller = CommonFormatController(project_code=project_code, file_system=fs)
    controller.write_met_station_input(site_level_dos=site_level_dos, met_station_dos=met_station_dos)
    controller.write_location_input(site_level_dos=site_level_dos)
    controller.write_electrical_input(site_level_dos=site_level_dos, combiner_dos=combiner_dos,
                                      inverter_dos=inverter_dos, shelter_dos=shelter_dos)
    controller.write_meter_box_input(site_level_dos=site_level_dos, meter_box_dos=meter_box_dos)
    controller.write_meas_input(tag_list_dos=tag_list_dos)
    controller.write_asset_list_input(combiner_dos=combiner_dos)
    controller.write_asset_info_input(inverter_dos=inverter_dos, combiner_dos=combiner_dos)
    logger.info(f'Done processing {s3_global_checklist}.')


# AWS Lambda does not call this method
if __name__ == '__main__':
    os.environ["S3_BUCKET_INPUTS"] = "edfred-edfre-sbx-s3-ew1-solar-site-onboarding-inputs"
    os.environ["S3_BUCKET_COMMON"] = "edfred-edfre-sbx-s3-ew1-solar-site-onboarding-common"
    # Project global checklist processing criteria:
    event_obj = {"projectCode": "BOUL", "dataColumnOffset": 3}
    # event_obj = {"projectCode": "MAV1", "dataColumnOffset": 3}
    # event_obj = {"projectCode": "MAV4", "dataColumnOffset": 3}
    # event_obj = {"projectCode": "DSH1", "dataColumnOffset": 3}
    # event_obj = {"projectCode": "DSH2", "dataColumnOffset": 3}
    handler(event_obj, {})
