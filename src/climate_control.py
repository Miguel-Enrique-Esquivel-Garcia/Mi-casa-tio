
from machine import Pin
import dht
import time

# --- SENSOR CONFIGURATION --

# SENSOR AL PIN D14 
sensor = dht.DHT11(Pin(14))  

# VENTILADOR AL PIN D5 
fan = Pin(5, Pin.OUT)

# TEMPERATURA MAXIMA 
temp_max = 25 

while True:
    try:
        sensor.measure()  # AQUI HACE LA LECTURA 
        temperature = sensor.temperature()  # °C
        humidity = sensor.humidity()         # %

        print("Temperature: {}°C  |  Humidity: {}%".format(temperature, humidity))

        if temperature >= temp_max:
            print("🔥 High temperature — Fan activated")
            fan.value(1)
        else:
            print("❄ Normal temperature — Turning off fan")
            fan.value(0)
            
    except OSError as e:
        print("ERROR READING THE SENSOR DHT11:", e)

    time.sleep(1)  
