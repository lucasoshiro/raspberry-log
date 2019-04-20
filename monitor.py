#!/usr/bin/env python3

from gpiozero import CPUTemperature
from psutil import cpu_percent

class Monitor:
    def __init__(self, *options):
        possible = {'temp', 'usage'}
        self.options = {*options}.intersection(possible) or possible
        
        if 'temp'  in self.options: self._cpu_temp = CPUTemperature()
        if 'usage' in self.options: cpu_percent(None)

    def cpu_temp(self):
        """ Return the current CPU temperature. """
        return self._cpu_temp.temperature

    def cpu_usage(self):
        """ Return the CPU usage since the last call. """
        return cpu_percent(None)

    def _get_result(self, option):
        return {
            'temp':  self.cpu_temp,
            'usage': self.cpu_usage
        }[option]()
        
    def all(self):
        """ Sample all monitored values. """
        return {option: self._get_result(option) for option in self.options}
