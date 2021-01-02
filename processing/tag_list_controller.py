import logging
from typing import List

from pandas import DataFrame

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.debug('Loading TagListController...')

logger.debug('Importing packages from relative path...')
from utils import Utils
from data_objects import TagListDO


class TagListController:

    def __init__(self):
        self.utils = Utils()

    def get_tag_list(self, dataframe: DataFrame, row_start: int, rows: int) -> List:
        logger.info('Getting Tag List data objects...')
        results = []
        for i in range(row_start, row_start + rows):

            tag_list_row = TagListDO(status=dataframe.iloc[i][0],
                                     operational_data=dataframe.iloc[i][1],
                                     pvps_level=dataframe.iloc[i][2],
                                     logical_device=dataframe.iloc[i][3],
                                     iec61850_logical_node=dataframe.iloc[i][4],
                                     scada_tag_name=dataframe.iloc[i][5],
                                     pointtype=dataframe.iloc[i][6],
                                     archiving=dataframe.iloc[i][7],
                                     compressing=dataframe.iloc[i][8],
                                     compdev=dataframe.iloc[i][9],
                                     compmax=dataframe.iloc[i][10],
                                     compmin=dataframe.iloc[i][11],
                                     compdevpercent=dataframe.iloc[i][12],
                                     excdev=dataframe.iloc[i][13],
                                     excmax=dataframe.iloc[i][14],
                                     excmin=dataframe.iloc[i][15],
                                     excdevpercent=dataframe.iloc[i][16],
                                     scan=dataframe.iloc[i][17],
                                     step=dataframe.iloc[i][18],
                                     convers=dataframe.iloc[i][19],
                                     filtercode=dataframe.iloc[i][20],
                                     value_type=dataframe.iloc[i][21],
                                     uom_conversion=dataframe.iloc[i][22],
                                     default_uom=dataframe.iloc[i][23],
                                     compressed_time_stamp=dataframe.iloc[i][24],
                                     average_10min=dataframe.iloc[i][25],
                                     count=dataframe.iloc[i][26],
                                     min=dataframe.iloc[i][27],
                                     max=dataframe.iloc[i][28],
                                     population_standard_deviation=dataframe.iloc[i][29],
                                     percentage_good_data=dataframe.iloc[i][30])

            if "Done" not in tag_list_row.status:
                continue

            results.append(tag_list_row)

        return results
