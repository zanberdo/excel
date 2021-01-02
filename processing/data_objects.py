import logging
from dataclasses import dataclass, field

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.debug('Loading data_objects dataclases...')

logger.debug('Importing packages from relative path...')
from utils import Utils


@dataclass(eq=True, frozen=False)
class SiteLevelDO:
    project_code: str
    iec_name: str
    latitude: str
    longitude: str
    module_tilt: str
    module_orientation: str
    capacity_limit_wac: int
    total_capacity_wdc: int
    number_of_feeders: int
    cod: str
    country: str = field(init=False)

    def __post_init__(self):
        utils = Utils()
        self.country = utils.get_country_by_lat_long(latitude=self.latitude, longitude=self.longitude)


@dataclass(eq=True, frozen=True)
class FeederDO:
    name: str
    iec_name: str
    capacity_wac: int
    capacity_wdc: int
    number_of_shelters_inverters: int
    cod: str
    contract_project_code: str


@dataclass(eq=True, frozen=True)
class ShelterDO:
    name: str
    iec_name: str
    capacity_wac: int
    capacity_wdc: int
    number_of_inverters_per_shelter: int
    parent_feeder: str


@dataclass(eq=True, frozen=True)
class InverterDO:
    name: str
    iec_name: str
    nominal_power_wac: int
    maximum_power_kwac: int
    total_dc_power: int
    states_and_fault_codes: str
    manufacturer: str
    model: str
    eventlist_name: str
    umpp_min: int
    umpp_max: int
    dc_max_voltage: int
    dc_max_current: int
    dc_max_power: int
    dc_nameplate: int
    dc_peak_power: int
    firmware_version: str
    dc_input_capacity: int
    number_of_connected_combiners: int
    module_manufacturer: str

    def get_unique_hash(self):
        return hash((self.maximum_power_kwac, self.nominal_power_wac, self.manufacturer, self.model))


@dataclass(eq=True, frozen=True)
class CombinerDO:
    name: str
    iec_name: str
    capacity_wdc: int
    manufacturer: str
    model: str
    temperature_coefficient: float
    contract_degradation_rate: float
    manufacturer_degradation_rate: float
    measured_degradation_rate: float


@dataclass(eq=True, frozen=True)
class SiteLevelNonElecDO:
    number_of_met_stations: int
    number_of_soiling_stations: int


@dataclass(eq=True, frozen=True)
class MetStationDO:
    name: str
    iec_name: str
    number_of_poa_sensors: int
    iec_pos_sensors: str
    number_of_rear_facing_sensors: int
    number_of_irradiance_sensors: int
    number_of_ghi_sensors: int
    number_of_bom_temp_sensors: int
    iec_bom_temperature_sensors: str
    number_of_ambient_temp_sensors: int


@dataclass(eq=True, frozen=True)
class SensorDO:
    name: str
    operating_range: str
    manufacturer: str
    model: str
    calibration_date: str
    calibration_value: str
    sensor_type: str


@dataclass(eq=True, frozen=True)
class SoilingStationDO:
    name: str
    soiling_rate: str
    last_cleaning_date: str
    last_calibration_date: str


@dataclass(eq=True, frozen=True)
class TrackerDO:
    name: str
    manufacturer: str
    model: str
    axis_orientation: str
    max_rotation_limit_east: str
    max_rotation_limit_west: str
    control_algorithm: str
    modules_on_tracker_row: int
    modules_layout_on_trackers: str
    post_to_post_separation: int
    stow_position_snow: str
    stow_position_wind: str
    block: str
    assoc_electrical_pvps: str
    controller_number: int
    motor_number: int
    row_height: int
    modules_per_row: int
    rows_per_motor: int


@dataclass(eq=True, frozen=True)
class MeterBoxDO:
    name: str
    iec_name: str
    deeper_level_asset_ref: str
    meterkind: str


@dataclass(eq=True, frozen=True)
class TagListDO:
    status: str
    operational_data: str
    pvps_level: str
    logical_device: str
    iec61850_logical_node: str
    scada_tag_name: str
    pointtype: str
    archiving: str
    compressing: str
    compdev: str
    compmax: str
    compmin: str
    compdevpercent: str
    excdev: str
    excmax: str
    excmin: str
    excdevpercent: str
    scan: str
    step: str
    convers: str
    filtercode: str
    value_type: str
    uom_conversion: str
    default_uom: str
    compressed_time_stamp: str
    average_10min: str
    count: str
    min: str
    max: str
    population_standard_deviation: str
    percentage_good_data: str
