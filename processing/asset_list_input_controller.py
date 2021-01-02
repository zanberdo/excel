import logging
from typing import List

import pandas as pd
from pandas import DataFrame

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.debug('Loading AssetListInputController...')

logger.debug('Importing packages from relative path...')
from data_objects import CombinerDO


class AssetListInputController:

    def __init__(self) -> None:
        self.columns = [
            'AssetInput',
            'AssetInfo_CombinerBoxB_DCPeakPower'
        ]

    def get_asset_list_dataframe(self, combiner_dos: List[CombinerDO]) -> DataFrame:
        logger.debug('get_asset_list_dataframe([combinerDOs)')
        rows = []
        for combiner_do in combiner_dos:
            asset_input = combiner_do.name
            asset_dc_peak_power = combiner_do.capacity_wdc
            rows.append(
                [asset_input,
                 asset_dc_peak_power]
            )
        dataframe = pd.DataFrame(data=rows, columns=self.columns)
        return dataframe
