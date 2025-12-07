"""
Code to activate buzzer and relay when MQ-2 exceeds 550
ESP32 MicroPython
"""

from machine import ADC, Pin
import utime

# --- MQ-2 SENSOR CONFIGURATION ---
AO_PIN = ADC(Pin(36))       # MQ-2 Analog Input (GPIO36 - ADC1_CH0)
AO_PIN.width(ADC.WIDTH_12BIT)
AO_PIN.atten(ADC.ATTN_11DB)

# --- OUTPUT CONFIGURATION ---
buzzer = Pin(15, Pin.OUT)    # GPIO15
rele = Pin(5, Pin.OUT)       # GPIO5

# Initially turned off
buzzer.value(0)
rele.value(0)

# --- PRINCIPAL LOOP ---
while True:
    gas_value = AO_PIN.read()   # Sensor reading
    print("MQ-2 Value:", gas_value)

    if gas_value > 550:   # Condition
        print("High level of contaminants detected. Alarm and extractor activated.")
        buzzer.value(1)
        rele.value(1)
    else:
        buzzer.value(0)
        rele.value(0)

    utime.sleep(1)
