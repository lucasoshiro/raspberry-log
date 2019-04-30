#!/usr/bin/env python3

from gpiozero import CPUTemperature
from psutil import cpu_percent

class CurrentSensor:
    def __init__(self):
        from ina219 import INA219
        self.ina219 = INA219(0.1)

    def current(self):
        """ Return the current in mA."""
        return ina219.current()

    def power(self):
        """ Return the power in mW"""
        return self.current() * 5

class Monitor:
    def __init__(self, *options):
        possible = {'temp', 'usage', 'power'}
        self.options = {*options}.intersection(possible) or possible
        
        if 'temp'  in self.options: self._cpu_temp = CPUTemperature()
        if 'usage' in self.options: cpu_percent(None)
        if 'power' in self.options: self.current_sensor = CurrentSensor()

    def cpu_temp(self):
        """ Return the current CPU temperature. """
        return self._cpu_temp.temperature

    def cpu_usage(self):
        """ Return the CPU usage since the last call. """
        return cpu_percent(None)

    def current(self):
        """ Return the current"""
        return self.current_sensor.current()

    def power(self):
        """ Return the power"""
        return self.current_sensor.power()

    def _get_result(self, option):
        return {
            'temp':  self.cpu_temp,
            'usage': self.cpu_usage
        }[option]()
        
    def all(self):
        """ Sample all monitored values. """
        return {option: self._get_result(option) for option in self.options}
