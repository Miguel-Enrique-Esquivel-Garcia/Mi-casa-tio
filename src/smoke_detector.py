"""
This ESP32 MicroPython code was developed by newbiely.com
This ESP32 MicroPython code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/esp32-micropython/esp32-micropython-gas-sensor
"""

from machine import ADC, Pin
import utime  # For timing functions

AO_PIN = ADC(Pin(36))  # The ESP32 pin GPIO36 (ADC0) as an analog input pin of the MQ2 gas sensor module
# Set the ADC width (resolution) to 12 bits
AO_PIN.width(ADC.WIDTH_12BIT)
# Set the attenuation to 11 dB, allowing input range up to ~3.3V
AO_PIN.atten(ADC.ATTN_11DB)

while True:
    gas_value = AO_PIN.read()  # Read the analog value (0-4095)

    print(gas_value)  # Print the analog value

    utime.sleep(1)  # Add a small delay to avoid spamming the output
