from contextlib import contextmanager


class SensorLessHomingHelper(object):
    def __init__(self, config):
        self.config = config
        self.printer = config.get_printer()
        self.toolhead = None
        self.gcode = self.printer.lookup_object('gcode')

        # Run current
        self.tmc_stepper_y_name = config.get('tmc_stepper_y_name')
        self.tmc_stepper_x_name = config.get('tmc_stepper_x_name')

        self.pconfig = self.printer.lookup_object("configfile")

        # Read config
        self.home_current = config.get('home_current')
        self.minimum_homing_distance = config.get('minimum_homing_distance', 5)
        self.retract_distance = config.get('retract_distance', 10)
        self.retract_speed = config.get('retract_speed', 20)
        self.stallguard_reset_time = config.get('stallguard_reset_time_ms', 1000)

        self.gcode.register_command('__HOME_X',
                                    self.cmd_HOME_X,
                                    'Sensorless homing X axis')
        self.gcode.register_command('__HOME_Y',
                                    self.cmd_HOME_Y,
                                    'Sensorless homing X axis')

        self.printer.register_event_handler('klippy:connect', self.handle_connect)

    def handle_connect(self):
        self.toolhead = self.printer.lookup_object('toolhead')

    @contextmanager
    def set_xy_motor_current(self, homing_current):
        x_stepper_name = self.tmc_stepper_x_name.split()[1]
        self.gcode.run_script_from_command(
            'SET_TMC_CURRENT STEPPER={} CURRENT={}'.format(x_stepper_name, homing_current))

        y_stepper_name = self.tmc_stepper_y_name.split()[1]
        self.gcode.run_script_from_command(
            'SET_TMC_CURRENT STEPPER={} CURRENT={}'.format(y_stepper_name, homing_current))

        try:
            yield
        finally:
            curtime = self.printer.get_reactor().monotonic()
            settings = self.pconfig.self.get_status(curtime)['settings']
            self.gcode.run_script_from_command(
                'SET_TMC_CURRENT STEPPER={} CURRENT={}'.format(x_stepper_name, settings[self.tmc_stepper_x_name]['run_current']))
            self.gcode.run_script_from_command(
                'SET_TMC_CURRENT STEPPER={} CURRENT={}'.format(y_stepper_name, settings[self.tmc_stepper_y_name]['run_current']))

    def cmd_HOME_X(self):
        # Check if X axis is homed and its last known position
        curtime = self.printer.get_reactor().monotonic()
        kin_status = self.toolhead.get_kinematics().get_status(curtime)

        pos = self.toolhead.get_position()

        if 'x' not in kin_status['homed_axes']:
            pos[0] = 0
            self.toolhead.set_position(pos, homing_axes=[0])
            self.toolhead.manual_move([None, None, -1 * self.minimum_homing_distance],
                                      self.retract_speed)
        elif kin_status['axis_maximum']['x'] - pos[0] < self.minimum_homing_distance:
            self.toolhead.manual_move([None, None, -1 * self.minimum_homing_distance],
                                      self.retract_speed)

    def cmd_HOME_Y(self):
        pass


def load_config(config):
    return SensorLessHomingHelper(config)
