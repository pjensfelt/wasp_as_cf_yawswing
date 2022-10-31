from __future__ import print_function

import sys
import time
import termios
import logging
import threading

import numpy as np
from cflib import crazyflie, crtp
from cflib.crazyflie.log import LogConfig

# Set a channel - if set to None, the first available crazyflie is used
URI = 'radio://0/83/2M'

def read_input(file=sys.stdin):
    """Registers keystrokes and yield these every time one of the
    *valid_characters* are pressed."""
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        while True:
            try:
                yield sys.stdin.read(1)
            except (KeyboardInterrupt, EOFError):
                break
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

class ControllerThread(threading.Thread):
    period_in_ms = 20  # Control period. [ms]

    # Are the motors enabled or not
    enabled = False

    # The stabilizer.yaw angle is supposed to track the reference value which switches between +45 and -45.
    yaw_ref = 45

    # Swing period in ms
    yaw_swing_period_ms = 10000

    # The max error in angle before you can switch reference yaw (+90 or -90) value
    yaw_err_max = 5

    # The current yaw value read from the Crazyflie
    yaw_curr = 0

    # The current battery voltage
    battery_volt = 0

    # The motor PWM control signals. These are the signals you should use to control the
    # yaw angle. These values are integers in the interval [0, 65535]
    motor_pwm1 = 0
    motor_pwm2 = 0
    motor_pwm3 = 0
    motor_pwm4 = 0

    def __init__(self, cf):
        super(ControllerThread, self).__init__()
        self.cf = cf
    
        # Keeps track of when we last printed
        self.last_time_print = 0.0

        # Connect some callbacks from the Crazyflie API
        self.cf.connected.add_callback(self._connected)
        self.cf.disconnected.add_callback(self._disconnected)
        self.cf.connection_failed.add_callback(self._connection_failed)
        self.cf.connection_lost.add_callback(self._connection_lost)
        self.send_setpoint = self.cf.commander.send_setpoint

        # This makes Python exit when this is the only thread alive.
        self.daemon = True

    def _connected(self, link_uri):
        print('Connected to', link_uri)

        log_stab_att = LogConfig(name='Stabilizer', period_in_ms=self.period_in_ms)
        log_stab_att.add_variable('stabilizer.yaw', 'float')
        self.cf.log.add_config(log_stab_att)
        
        log_batt = LogConfig(name='Battery', period_in_ms=self.period_in_ms)
        log_batt.add_variable('pm.vbat', 'float')
        self.cf.log.add_config(log_batt)
        
        if log_stab_att.valid and log_batt.valid:
            log_stab_att.data_received_cb.add_callback(self._log_data_stab_att)
            log_stab_att.error_cb.add_callback(self._log_error)
            log_stab_att.start()

            log_batt.data_received_cb.add_callback(self._log_data_batt)
            log_batt.error_cb.add_callback(self._log_error)
            log_batt.start()

        else:
            raise RuntimeError('One or more of the variables in the configuration was not found in log TOC.')

    def _connection_failed(self, link_uri, msg):
        print('Connection to %s failed: %s' % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        print('Disconnected from %s' % link_uri)

    def _log_data_stab_att(self, timestamp, data, logconf):
        self.yaw_curr = data['stabilizer.yaw'];
    
    def _log_data_batt(self, timestamp, data, logconf):
        self.battery_volt = data['pm.vbat'];
    
    def _log_error(self, logconf, msg):
        print('Error when logging %s: %s' % (logconf.name, msg))

    def run(self):
        print('Wating for a connection')
        while not self.cf.is_connected():
            time.sleep(0.2)

        # Make sure we are disabled
        self.disable()

        print('Waiting for position estimate to be good enough...')
        self.reset_estimator()

        print('Ready! Press e to enable motors, h for help and Q to quit')
        log_file_name = 'log_' + time.strftime("%Y%m%d_%H%M%S") + '.csv'
        with open(log_file_name, 'w') as fh:
            t0 = time.time()
            while True:

                time_start = time.time()

                # See if it is time to switch the reference value
                t_ms = int(1000.0 * (time_start - t0));
                if self.yaw_ref > 0:
                    if t_ms % self.yaw_swing_period_ms > self.yaw_swing_period_ms / 2:
                        self.yaw_ref = -self.yaw_ref
                else:
                    if t_ms % self.yaw_swing_period_ms <= self.yaw_swing_period_ms / 2:
                        self.yaw_ref = -self.yaw_ref

                # Calculate the control signals
                self.calc_control_signals()

                # If Send the control signals
                if self.enabled:
                    self.cf.param.set_value("motorPowerSet.m1", self.motor_pwm1)
                    self.cf.param.set_value("motorPowerSet.m2", self.motor_pwm2)
                    self.cf.param.set_value("motorPowerSet.m3", self.motor_pwm3)
                    self.cf.param.set_value("motorPowerSet.m4", self.motor_pwm4)

                # Log data to file
                if self.enabled:
                    # Log data to file for analysis
                    ld = np.r_[time.time() - t0]
                    ld = np.append(ld, self.yaw_curr)
                    ld = np.append(ld, self.yaw_ref)
                    ld = np.append(ld, self.enabled)
                    ld = np.append(ld, self.motor_pwm1)
                    ld = np.append(ld, self.motor_pwm2)
                    ld = np.append(ld, self.motor_pwm3)
                    ld = np.append(ld, self.motor_pwm4)
                    ld = np.append(ld, self.battery_volt)
                    fh.write(';'.join(map(str, ld)) + '\n')
                    fh.flush()
                
                # Sleep a while so that we keep a certain control frequency
                self.loop_sleep(time_start)

    def limit_pwm(self, pwm):
        if pwm < 0:
            pwm = 0
        elif pwm > 0XFFFF:
            pwm = 0XFFFF
        return pwm

    # Calculates the difference between two angles taking care of cases such as 359 - 1 = 2 and NOT 358
    def angle_difference(self, ang1, ang2):
        diff = ang1 - ang2
        if (diff > 180):
            diff -= 360
        if (diff < -360):
            diff += 360
        return diff

    def calc_control_signals(self):
        # Calculate the error between the reference yaw signal and the current yaw
        yaw_err = self.angle_difference(self.yaw_ref, self.yaw_curr)

        # YOUR CODE STARTS HERE
        # THIS IS WHERE YOU SHOULD PUT YOUR CONTROL CODE
        # THAT OUTPUTS THE REFERENCE VALUES THE MOTOR PWM VALUES
        # In the code below set the variables m1, m2, m3, m4 appropriately
        # The shoild each take on values in [0,65535] which is taken care of
        # by the function limit_pwm

        m1 = 10000;
        m2 = 10000;
        m3 = 10000;
        m4 = 10000;

        # YOUR CODE ENDS HERE

        # Set the control variables and make sure that they are integers and between 0 and 65535
        self.motor_pwm1 = self.limit_pwm(int(m1))
        self.motor_pwm2 = self.limit_pwm(int(m2))
        self.motor_pwm3 = self.limit_pwm(int(m3))
        self.motor_pwm4 = self.limit_pwm(int(m4))
    
        # Print debugging message on the screen for easier debugging
        message = ('yaw: (curr={}, ref={}, err={}),   battery:{:.3}V\n'.format(self.yaw_curr, self.yaw_ref, yaw_err, self.battery_volt) +
                   '     control: ({}, {}, {}, {}, {})\n'.format(self.enabled, self.motor_pwm1, self.motor_pwm2, self.motor_pwm3, self.motor_pwm4))
        self.print_at_period(1.0, message)



    def print_at_period(self, period, message):
        """ Prints the message at a given period """
        if (time.time() - period) >  self.last_time_print:
            self.last_time_print = time.time()
            print(message)

    def reset_estimator(self):
        self.cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        self.cf.param.set_value('kalman.resetEstimation', '0')
        # Sleep a bit, hoping that the estimator will have converged
        # Should be replaced by something that actually checks...
        time.sleep(1.5)

    def disable(self):
        print('Disabling controller')
        self.enabled = False
        self.cf.param.set_value("motorPowerSet.enable", '0')

    def enable(self):
        print('Enabling controller')
        self.enabled = True
        self.cf.param.set_value("motorPowerSet.enable", '1')

    def loop_sleep(self, time_start):
        """ Sleeps the control loop to make it run at a specified rate """
        delta_time = 1e-3*self.period_in_ms - (time.time() - time_start)
        if delta_time > 0:
            time.sleep(delta_time)
        else:
            print('Deadline missed by', -delta_time, 'seconds. '
                  'Too slow control loop!')

def handle_keyboard_input(control):
    for ch in read_input():
        if ch == 'e':
            control.enable()
        elif ch == 'd':
            if not control.enabled:
                print('Uppercase Q quits the program')
            control.disable()
        elif ch == 'Q':
            control.disable()
            time.sleep(0.5)
            print('Bye!')
            break
        else:
            print('Unhandled key', ch, 'was pressed')
            print('Key map:')
            print('Q: quit program')
            print('e: Enable motors')
            print('d: Disable motors')

if __name__ == "__main__":
    logging.basicConfig()
    crtp.init_drivers(enable_debug_driver=False)
    cf = crazyflie.Crazyflie(rw_cache='./cache')
    control = ControllerThread(cf)
    control.start()

    print('Connecting to', URI)
    cf.open_link(URI)

    # Read key board input as a way to determine how long the control loop should run
    handle_keyboard_input(control)

    cf.close_link()
