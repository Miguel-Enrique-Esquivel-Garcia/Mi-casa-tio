#main.py de la esp32 

import machine
import network
import time
from machine import Pin
from umqtt_simple import MQTTClient

# ===== CONFIGURACIÓN DE RED =====
WIFI_SSID = "Totalplay-2.4G-da18"
WIFI_PASSWORD = "ruJAFxN7U2SVG5yS"

# ===== CONFIGURACIÓN MQTT =====
MQTT_BROKER = "192.168.100.51"  # Puedes usar tu propio broker
MQTT_PORT = 1883
MQTT_CLIENT_ID = "micropython_led"
MQTT_TOPIC = b"casa/sala/led"

# ===== CONFIGURACIÓN DEL LED =====
led = Pin(21, Pin.OUT)  # GPIO2 en ESP32/ESP8266 (LED integrado)

# ===== FUNCIÓN PARA CONECTAR WIFI =====
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print("Conectado a WiFi:", wlan.ifconfig())
    else:
        raise RuntimeError("No se pudo conectar a WiFi")

# ===== CALLBACK CUANDO LLEGA UN MENSAJE =====
def mensaje_mqtt(topic, msg):
    print("Mensaje recibido:", topic, msg)
    if msg == b"ON":
        led.value(1)
    elif msg == b"OFF":
        led.value(0)

# ===== PROGRAMA PRINCIPAL =====
def main():
    try:
        conectar_wifi()

        cliente = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        cliente.set_callback(mensaje_mqtt)
        cliente.connect()
        print("Conectado al broker MQTT:", MQTT_BROKER)

        cliente.subscribe(MQTT_TOPIC)
        print("Suscrito al tópico:", MQTT_TOPIC)

        while True:
            cliente.check_msg()  # Revisa si hay mensajes nuevos
            time.sleep(0.1)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
        machine.reset()  # Reinicia el microcontrolador en caso de fallo

# ===== EJECUCIÓN =====
if __name__ == "__main__":
    main()
