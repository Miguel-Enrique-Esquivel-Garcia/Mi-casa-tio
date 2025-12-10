# MicroPython INA219 Library
# Simplified version for ESP32

from machine import I2C
import time

class INA219:
    def __init__(self, shunt_ohms, i2c, address=0x40):
        self._i2c = i2c
        self._address = address
        self._shunt = shunt_ohms
        self._calibration_value = 4096

        self._write_register(0x00, 0x399F)  # config register
        self._write_register(0x05, self._calibration_value)

    def _write_register(self, reg, value):
        self._i2c.writeto_mem(self._address, reg, value.to_bytes(2, 'big'))

    def _read_register(self, reg):
        data = self._i2c.readfrom_mem(self._address, reg, 2)
        return int.from_bytes(data, 'big')

    def shunt_voltage(self):
        val = self._read_register(0x01)
        if val > 32767:
            val -= 65536
        return val * 0.01  # mV

    def bus_voltage(self):
        val = self._read_register(0x02)
        return (val >> 3) * 0.004  # V

    def current(self):
        val = self._read_register(0x04)
        if val > 32767:
            val -= 65536
        return val * 0.1  # mA

    def power(self):
        val = self._read_register(0x03)
        return val * 2  # mW
