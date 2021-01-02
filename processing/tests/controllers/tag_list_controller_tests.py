import logging
import unittest

import pandas as pd

from processing.data_objects import TagListDO
from processing.tag_list_controller import TagListController

MSG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(format=MSG_FORMAT, datefmt=DATETIME_FORMAT)
logger = logging.getLogger("tag_list_controller_tests")
logger.setLevel(logging.INFO)


class TagListControllerTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.controller = TagListController()

    def tearDown(self) -> None:
        pass
        # self.patcher.stop()

    def build_input_object(self, rows=1):
        return {
            "status": ["status" for i in range(0, rows)],
            "operational_data": ["operational_data" for i in range(0, rows)],
            "pvps_level": ["pvps_level" for i in range(0, rows)],
            "logical_device": ["logical_device" for i in range(0, rows)],
            "iec61850_logical_node": ["iec61850_logical_node" for i in range(0, rows)],
            "scada_tag_name": ["scada_tag_name" for i in range(0, rows)],
            "pointtype": ["pointtype" for i in range(0, rows)],
            "archiving": ["archiving" for i in range(0, rows)],
            "compressing": ["compressing" for i in range(0, rows)],
            "compdev": ["compdev" for i in range(0, rows)],
            "compmax": ["compmax" for i in range(0, rows)],
            "compmin": ["compmin" for i in range(0, rows)],
            "compdevpercent": ["compdevpercent" for i in range(0, rows)],
            "excdev": ["excdev" for i in range(0, rows)],
            "excmax": ["excmax" for i in range(0, rows)],
            "excmin": ["excmin" for i in range(0, rows)],
            "excdevpercent": ["excdevpercent" for i in range(0, rows)],
            "scan": ["scan" for i in range(0, rows)],
            "step": ["step" for i in range(0, rows)],
            "convers": ["convers" for i in range(0, rows)],
            "filtercode": ["filtercode" for i in range(0, rows)],
            "value_type": ["value_type" for i in range(0, rows)],
            "uom_conversion": ["uom_conversion" for i in range(0, rows)],
            "default_uom": ["default_uom" for i in range(0, rows)],
            "compressed_time_stamp": ["compressed_time_stamp" for i in range(0, rows)],
            "average_10min": ["average_10min" for i in range(0, rows)],
            "count": ["count" for i in range(0, rows)],
            "min": ["min" for i in range(0, rows)],
            "max": ["max" for i in range(0, rows)],
            "population_standard_deviation": ["population_standard_deviation" for i in range(0, rows)],
            "percentage_good_data": ["percentage_good_data" for i in range(0, rows)]
        }

    def build_tag_list_do(self,
                          status="status",
                          operational_data="operational_data",
                          pvps_level="pvps_level",
                          logical_device="logical_device",
                          iec61850_logical_node="iec61850_logical_node",
                          scada_tag_name="scada_tag_name",
                          pointtype="pointtype",
                          archiving="archiving",
                          compressing="compressing",
                          compdev="compdev",
                          compmax="compmax",
                          compmin="compmin",
                          compdevpercent="compdevpercent",
                          excdev="excdev",
                          excmax="excmax",
                          excmin="excmin",
                          excdevpercent="excdevpercent",
                          scan="scan",
                          step="step",
                          convers="convers",
                          filtercode="filtercode",
                          value_type="value_type",
                          uom_conversion="uom_conversion",
                          default_uom="default_uom",
                          compressed_time_stamp="compressed_time_stamp",
                          average_10min="average_10min",
                          count="count",
                          min="min",
                          max="max",
                          population_standard_deviation="population_standard_deviation",
                          percentage_good_data="percentage_good_data"):
        return TagListDO(
            status=status,
            operational_data=operational_data,
            pvps_level=pvps_level,
            logical_device=logical_device,
            iec61850_logical_node=iec61850_logical_node,
            scada_tag_name=scada_tag_name,
            pointtype=pointtype,
            archiving=archiving,
            compressing=compressing,
            compdev=compdev,
            compmax=compmax,
            compmin=compmin,
            compdevpercent=compdevpercent,
            excdev=excdev,
            excmax=excmax,
            excmin=excmin,
            excdevpercent=excdevpercent,
            scan=scan,
            step=step,
            convers=convers,
            filtercode=filtercode,
            value_type=value_type,
            uom_conversion=uom_conversion,
            default_uom=default_uom,
            compressed_time_stamp=compressed_time_stamp,
            average_10min=average_10min,
            count=count,
            min=min,
            max=max,
            population_standard_deviation=population_standard_deviation,
            percentage_good_data=percentage_good_data)

    def test_get_tag_list_returns_list_of_tag_list_dos(self):
        expected = [self.build_tag_list_do(status="Done"), self.build_tag_list_do(status="Done")]
        input_df = pd.DataFrame(self.build_input_object(rows=2))
        row_start = 0
        rows = 2

        input_df["status"][0] = "Done"
        input_df["status"][1] = "Done"

        actual = self.controller.get_tag_list(dataframe=input_df, row_start=row_start, rows=rows)
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0], actual[0])

    def test_get_tag_list_skips_rows_without_done_status(self):
        expected = [self.build_tag_list_do(status="Done")]
        input_df = pd.DataFrame(self.build_input_object(rows=2))
        row_start = 0
        rows = 2

        input_df["status"][1] = "Done"

        actual = self.controller.get_tag_list(dataframe=input_df, row_start=row_start, rows=rows)
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0], actual[0])

    def test_get_tag_list_skips_rows_before_row_start(self):
        expected = [self.build_tag_list_do(status="Done")]
        input_df = pd.DataFrame(self.build_input_object(rows=2))
        row_start = 1
        rows = 1

        input_df["status"][0] = "Done"
        input_df["status"][1] = "Done"

        actual = self.controller.get_tag_list(dataframe=input_df, row_start=row_start, rows=rows)
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0], actual[0])

    def test_get_tag_list_processes_number_of_rows_specified_by_rows_param(self):
        expected = [self.build_tag_list_do(status="Done")]
        input_df = pd.DataFrame(self.build_input_object(rows=2))
        row_start = 0
        rows = 1

        input_df["status"][0] = "Done"
        input_df["status"][1] = "Done"

        actual = self.controller.get_tag_list(dataframe=input_df, row_start=row_start, rows=rows)
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0], actual[0])


if __name__ == '__main__':
    unittest.main()
