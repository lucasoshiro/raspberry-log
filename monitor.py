#!/usr/bin/env python3

from time import time

class CurrentSensor:
    def __init__(self):
        from ina219 import INA219
        self.ina219 = INA219(0.1)
        self.ina219.configure()

    def current(self):
        """ Return the current in mA."""
        return self.ina219.current()

    def power(self):
        """ Return the power in mW"""
        return self.current() * 5

class CPUSensor:
    def __init__(self):
        from psutil import cpu_percent
        self.cpu_percent = lambda *_: cpu_percent(*_)

    def usage(self):
        return self.cpu_percent(None)

class TempSensor:
    def __init__(self):
        from gpiozero import CPUTemperature
        self._cpu_temp = CPUTemperature()

    def temperature(self):
        return self._cpu_temp.temperature

class RAMSensor:
    def __init__(self):
        from psutil import virtual_memory
        self.virtual_memory = virtual_memory

    def used(self):
        return self.virtual_memory().used

class Monitor:
    def __init__(self, options):
        possible = {'temp', 'usage', 'power', 'ram'}
        self.options = {*options}.intersection(possible) or possible
        
        if 'temp'  in self.options: self.temp_sensor = CPUTemperature()
        if 'usage' in self.options: self.cpu_sensor = CPUSensor()
        if 'power' in self.options: self.current_sensor = CurrentSensor()
        if 'ram'   in self.options: self.ram_sensor = RAMSensor()

    def cpu_temp(self):
        """ Return the current CPU temperature. """
        return self.temp_sensor.temperature()

    def cpu_usage(self):
        """ Return the CPU usage since the last call. """
        return self.cpu_sensor.usage()

    def current(self):
        """ Return the current"""
        return self.current_sensor.current()

    def power(self):
        """ Return the power"""
        return self.current_sensor.power()

    def ram(self):
        """ Return the RAM usage """
        return self.ram_sensor.used()

    def _get_result(self, option):
        return {
            'temp':  self.cpu_temp,
            'usage': self.cpu_usage,
            'power': self.power,
            'ram':   self.ram
        }[option]()
        
    def all(self):
        """ Sample all monitored values. """
        sample = {option: self._get_result(option) for option in self.options}
        sample['timestamp'] = time()
        return sample
