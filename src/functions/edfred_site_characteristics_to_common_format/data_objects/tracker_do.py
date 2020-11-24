class TrackerDO:

    def __init__(self,
                 name,
                 manufacturer,
                 model,
                 axis_orientation,
                 max_rotation_limit_east,
                 max_rotation_limit_west,
                 control_algorithm,
                 modules_on_tracker_row,
                 modules_layout_on_trackers,
                 post_to_post_separation,
                 stow_position_snow,
                 stow_position_wind,
                 block,
                 assoc_electrical_pvps,
                 controller_number,
                 motor_number,
                 row_height,
                 modules_per_row,
                 rows_per_motor
                 ):
        self.name = name
        self.manufacturer = manufacturer
        self.model = model
        self.axis_orientation = axis_orientation
        self.max_rotation_limit_east = max_rotation_limit_east
        self.max_rotation_limit_west = max_rotation_limit_west
        self.control_algorithm = control_algorithm
        self.modules_on_tracker_row = modules_on_tracker_row
        self.modules_layout_on_trackers = modules_layout_on_trackers
        self.post_to_post_separation = post_to_post_separation
        self.stow_position_snow = stow_position_snow
        self.stow_position_wind = stow_position_wind
        self.block = block
        self.assoc_electrical_pvps = assoc_electrical_pvps
        self.controller_number = controller_number
        self.motor_number = motor_number
        self.row_height = row_height
        self.modules_per_row = modules_per_row
        self.rows_per_motor = rows_per_motor

    def __repr__(self) -> str:
        results = '{\n\t"TrackerDO" : {\n'
        for attr, value in self.__dict__.items():
            if type(value) is int:
                results += f'\t\t"{attr}": {value},\n'
            else:
                results += f'\t\t"{attr}": "{value}",\n'
        return results[:-2] + "\n\t}" + "\n}"
