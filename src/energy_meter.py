from ina219 import INA219
from machine import I2C, Pin

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
ina = INA219(0.1, i2c, address=0x40)  # cambia si tu dirección es otra

print("Voltaje:", ina.bus_voltage())
print("Corriente:", ina.current())
print("Potencia:", ina.power())