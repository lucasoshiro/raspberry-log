#!/usr/bin/env python3

from time import time

class CurrentSensor:
    def __init__(self):
        from ina219 import INA219
        self.ina219 = INA219(0.1)
        self.ina219.configure()

    def current(self):
        """ Return the current in mA. """
        return self.ina219.current()

    def power(self):
        """ Return the power in mW. """
        return self.current() * 5

class CPUSensor:
    def __init__(self):
        from psutil import cpu_percent
        self._cpu_percent = lambda *_: cpu_percent(*_)

    def usage(self):
        """ Return the CPU usage, in percent. """
        return self._cpu_percent(None)

class TempSensor:
    def __init__(self):
        from gpiozero import CPUTemperature
        self._cpu_temp = CPUTemperature()

    def temperature(self):
        """ Return the CPU temperature, in degrees celsius. """
        return self._cpu_temp.temperature

class RAMSensor:
    def __init__(self):
        from psutil import virtual_memory
        self._virtual_memory = virtual_memory

    def used(self):
        """ Return the used virtual memory, in bytes. """
        return self._virtual_memory().used

class NetSensor:
    def __init__(self):
        from psutil import net_io_counters
        self._net_io_counters = net_io_counters

        n0 = self._net_io_counters()
        t = time()

        self.last_sample = {
            'down': (t, n0.bytes_recv),
            'up': (t, n0.bytes_sent)
        }

    def calculate_rate(self, field, callback):
        t1, s1 = time(), callback()
        t0, s0 = self.last_sample[field]

        rate = (s1 - s0) / (t1 - t0)

        self.last_sample[field] = (t1, s1)

        return rate

    def download_rate(self):
        return self.calculate_rate(
            'down', lambda: self._net_io_counters().bytes_recv)

    def upload_rate(self):
        return self.calculate_rate(
            'up', lambda: self._net_io_counters().bytes_sent)

class Monitor:
    def __init__(self, options):
        possible = {'temp', 'usage', 'power', 'ram', 'net_down', 'net_up'}
        self.options = {*options}.intersection(possible) or possible

        if 'temp'     in self.options: self.temp_sensor    = TempSensor()
        if 'usage'    in self.options: self.cpu_sensor     = CPUSensor()
        if 'power'    in self.options: self.current_sensor = CurrentSensor()
        if 'ram'      in self.options: self.ram_sensor     = RAMSensor()

        if {'net_down', 'net_up'}.intersection(self.options):
            self.net_sensor = NetSensor()

    def cpu_temp(self):
        """ Return the current CPU temperature, in degrees Celsius. """
        return self.temp_sensor.temperature()

    def cpu_usage(self):
        """ Return the CPU usage since the last call. """
        return self.cpu_sensor.usage()

    def current(self):
        """ Return the current in mA. """
        return self.current_sensor.current()

    def power(self):
        """ Return the power in mW. """
        return self.current_sensor.power()

    def ram(self):
        """ Return the RAM usage in bytes. """
        return self.ram_sensor.used()

    def net_down(self):
        """ Return the download rate in bytes per second. """
        return self.net_sensor.download_rate()

    def net_up(self):
        """ Return the upload rate in bytes per second. """
        return self.net_sensor.upload_rate()

    def _get_result(self, option):
        return {
            'temp':     self.cpu_temp,
            'usage':    self.cpu_usage,
            'power':    self.power,
            'ram':      self.ram,
            'net_down': self.net_down,
            'net_up':   self.net_up

        }[option]()

    def all(self):
        """ Sample all monitored values. """
        sample = {option: self._get_result(option) for option in self.options}
        sample['timestamp'] = time()
        return sample
