#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
# Notice
#   1. Changes to this file on Studio will not be preserved
#   2. The next conversion will overwrite the file with the same name
# 
# xArm-Python-SDK: https://github.com/xArm-Developer/xArm-Python-SDK
#   1. git clone git@github.com:xArm-Developer/xArm-Python-SDK.git
#   2. cd xArm-Python-SDK
#   3. python setup.py install
"""
import sys
import math
import time
import queue
import datetime
import random
import traceback
import threading
from xarm import version
from xarm.wrapper import XArmAPI


class RobotMain(object):
    """Robot Main Class"""
    def __init__(self, robot, **kwargs):
        self.alive = True
        self._arm = robot
        self._tcp_speed = 100
        self._tcp_acc = 2000
        self._angle_speed = 20
        self._angle_acc = 500
        self._variables = {}
        self._robot_init()
        self._arm.set_cartesian_velo_continuous(True)

    # Robot init
    def _robot_init(self):
        self._arm.clean_warn()
        self._arm.clean_error()
        self._arm.motion_enable(True)
        self._arm.set_mode(0)
        self._arm.set_state(0)
        time.sleep(1)
        self._arm.register_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.register_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'register_count_changed_callback'):
            self._arm.register_count_changed_callback(self._count_changed_callback)

    # Register error/warn changed callback
    def _error_warn_changed_callback(self, data):
        if data and data['error_code'] != 0:
            self.alive = False
            self.pprint('err={}, quit'.format(data['error_code']))
            self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)

    # Register state changed callback
    def _state_changed_callback(self, data):
        if data and data['state'] == 4:
            self.alive = False
            self.pprint('state=4, quit')
            self._arm.release_state_changed_callback(self._state_changed_callback)

    # Register count changed callback
    def _count_changed_callback(self, data):
        if self.is_alive:
            self.pprint('counter val: {}'.format(data['count']))

    def _check_code(self, code, label):
        if not self.is_alive or code != 0:
            self.alive = False
            ret1 = self._arm.get_state()
            ret2 = self._arm.get_err_warn_code()
            self.pprint('{}, code={}, connected={}, state={}, error={}, ret1={}. ret2={}'.format(label, code, self._arm.connected, self._arm.state, self._arm.error_code, ret1, ret2))
        return self.is_alive

    @staticmethod
    def pprint(*args, **kwargs):
        try:
            stack_tuple = traceback.extract_stack(limit=2)[0]
            print('[{}][{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1], ' '.join(map(str, args))))
        except:
            print(*args, **kwargs)

    @property
    def is_alive(self):
        if self.alive and self._arm.connected and self._arm.error_code == 0:
            if self._arm.state == 5:
                cnt = 0
                while self._arm.state == 5 and cnt < 5:
                    cnt += 1
                    time.sleep(0.1)
            return self._arm.state < 4
        else:
            return False

    # Robot Main Run
    def run(self):
        try:
            self._angle_acc = 500
            self._angle_speed = 180
            self._tcp_speed = 450
            self._tcp_acc = 2000
            code = self._arm.set_cgpio_digital(5, 1, delay_sec=0)
            if not self._check_code(code, 'set_cgpio_digital'):
                return
            code = self._arm.set_servo_angle(angle=[189.2, 80.2, 85.2, 16.8, -104.5, 169.9], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            code = self._arm.set_position(*[5.0, -20.0, 10.0, 180.0, 15.0, 83.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            self._tcp_speed = 150
            code = self._arm.set_cgpio_digital(1, 1, delay_sec=0)
            if not self._check_code(code, 'set_cgpio_digital'):
                return
            code = self._arm.set_position(*[62.0, -5.0, 14.0, 180.0, 15.0, 135.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[85.5, 40.8, 12.9, 180.0, 15.0, 163.5], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            self._tcp_speed = 75
            code = self._arm.set_position(*[92.2, 76.8, 12.0, 180.0, 15.0, 168.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[103.9, 123.3, 14.0, 180.0, 15.0, 164.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[117.3, 177.7, 13.0, 180.0, 15.0, 175.4], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[115.5, 229.8, 9.7, 180.0, 15.0, -171.8], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            self._tcp_speed = 150
            code = self._arm.set_position(*[107.1, 259.0, 9.9, 180.0, 15.0, -158.7], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[88.4, 296.1, 7.0, 180.0, 15.0, -137.4], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[44.5, 318.0, 5.0, 180.0, 15.0, -101.7], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-11.4, 305.0, 6.0, 180.0, 15.0, -52.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-33.1, 273.3, 5.6, 180.0, 15.0, -32.2], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-50.4, 234.2, 12.0, 180.0, 15.0, -12.7], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            self._tcp_speed = 75
            code = self._arm.set_position(*[-57.8, 187.4, 12.8, 180.0, 15.0, -1.3], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-52.5, 140.5, 12.7, 180.0, 15.0, -2.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-55.0, 103.8, 11.0, 180.0, 15.0, -8.1], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[-64.0, 63.5, 11.0, 180.0, 15.0, -3.7], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            self._tcp_speed = 150
            code = self._arm.set_position(*[-51.2, 5.0, 15.4, 180.0, 15.0, 35.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_position(*[5.0, -25.0, 13.0, 180.0, 15.0, 83.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            code = self._arm.set_cgpio_digital(1, 0, delay_sec=0)
            if not self._check_code(code, 'set_cgpio_digital'):
                return
            self._tcp_speed = 500
            code = self._arm.set_servo_angle(angle=[189.2, 80.2, 85.2, 16.8, -104.5, 169.9], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            code = self._arm.set_cgpio_digital(5, 0, delay_sec=0)
            if not self._check_code(code, 'set_cgpio_digital'):
                return
        except Exception as e:
            self.pprint('MainException: {}'.format(e))
        self.alive = False
        self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.release_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'release_count_changed_callback'):
            self._arm.release_count_changed_callback(self._count_changed_callback)


if __name__ == '__main__':
    RobotMain.pprint('xArm-Python-SDK Version:{}'.format(version.__version__))
    arm = XArmAPI('192.168.1.227', baud_checkset=False)
    robot_main = RobotMain(arm)
    robot_main.run()
