# main.py — ESP32 + MicroPython
# Wi-Fi + MQTT (control de LED) + MQ-2 + sensor de lluvia + servo + DHT11 + relevador

import machine
import network
import time
from machine import Pin, ADC, PWM
from umqtt_simple import MQTTClient
import dht

# ======================================================================
# ---------------------  CONFIGURACIÓN DE RED  -------------------------
# ======================================================================

WIFI_SSID = "POCO X6 Pro 5G"
WIFI_PASSWORD = "paulo1234"

# ======================================================================
# ----------------------  CONFIGURACIÓN MQTT  --------------------------
# ======================================================================

MQTT_BROKER = "10.70.87.205"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "micropython_led"
MQTT_TOPIC = b"casa/sala/led"

# LED controlado por MQTT
led = Pin(21, Pin.OUT)   # LED en GPIO 21

# ======================================================================
# -------------------------  MQ-2 (GAS)  -------------------------------
# ======================================================================

AO_PIN = ADC(Pin(36))              # Entrada analógica para MQ-2
AO_PIN.width(ADC.WIDTH_12BIT)
AO_PIN.atten(ADC.ATTN_11DB)

buzzer = Pin(15, Pin.OUT)          # Buzzer
relay = Pin(5, Pin.OUT)            # Relevador (ventilador / extractor)

buzzer.value(0)
relay.value(0)

# ======================================================================
# ------------------  SENSOR DE LLUVIA + SERVO  ------------------------
# ======================================================================

rain = Pin(4, Pin.IN)              # Sensor de lluvia

servo = PWM(Pin(13), freq=50)      # Servo en GPIO 13 a 50 Hz

OPEN_ANGLE = 90
CLOSED_ANGLE = 0

def move_servo(angle):
    # Conversión de ángulo a ciclo de trabajo aproximado
    duty = int((angle / 180 * 75) + 40)
    servo.duty(duty)

# ======================================================================
# -----------------------------  DHT11  --------------------------------
# ======================================================================

sensor = dht.DHT11(Pin(14))        # DHT11 en GPIO 14
TEMP_MAX = 30                      # Umbral de temperatura (°C)

# ======================================================================
# ---------------------  CONEXIÓN A WIFI  ------------------------------
# ======================================================================

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

# ======================================================================
# ---------------------  CALLBACK MQTT (LED)  --------------------------
# ======================================================================

def mensaje_mqtt(topic, msg):
    print("Mensaje recibido:", topic, msg)
    if msg == b"ON":
        led.value(1)
    elif msg == b"OFF":
        led.value(0)

# ======================================================================
# ---------------------------  PROGRAMA  -------------------------------
# ======================================================================

def main():
    try:
        # 1) Conectar WiFi
        conectar_wifi()

        # 2) Configurar MQTT
        cliente = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        cliente.set_callback(mensaje_mqtt)
        cliente.connect()
        print("Conectado al broker MQTT:", MQTT_BROKER)

        cliente.subscribe(MQTT_TOPIC)
        print("Suscrito al tópico:", MQTT_TOPIC)

        # 3) Estado inicial de actuadores
        led.value(0)
        buzzer.value(0)
        relay.value(0)
        move_servo(OPEN_ANGLE)

        print("🌡🌧🔥 SYSTEM ONLINE — MULTI-SENSOR CONTROL + MQTT LED")

        # 4) Bucle principal
        while True:
            # ---------------- MQTT (LED) ----------------
            # Revisa si hay mensajes nuevos para el LED
            cliente.check_msg()

            # ---------------- MQ-2 GAS SENSOR ----------------
            gas_value = AO_PIN.read()
            print("MQ-2 Value:", gas_value)

            if gas_value > 550:
                print("⚠ High GAS — Alarm + Ventilator ON")
                buzzer.value(1)
                relay.value(1)  # Relevador encendido por gas
            else:
                buzzer.value(0)
                # El relevador se apaga en la sección de temperatura
                # solo si gas también está en niveles normales.

            # ---------------- SENSOR DE LLUVIA + SERVO ----------------
            rain_state = rain.value()

            if rain_state == 0:
                print("🌧 Rain detected — Closing window")
                move_servo(CLOSED_ANGLE)
            else:
                print("☀ No rain — Opening window")
                move_servo(OPEN_ANGLE)

            # ---------------- DHT11 TEMPERATURE ----------------
            try:
                sensor.measure()
                temperature = sensor.temperature()
                humidity = sensor.humidity()

                print("Temp: {}°C | Humidity: {}%".format(temperature, humidity))

                if temperature >= TEMP_MAX:
                    print("🔥 High temp — Ventilator ON")
                    relay.value(1)     # Relevador encendido por temperatura
                else:
                    print("❄ Normal temp")
                    # Apagar relevador SOLO si el gas también está en rango seguro
                    if gas_value <= 550:
                        relay.value(0)

            except OSError as e:
                print("❌ ERROR DHT11:", e)

            print("-----------------------------------")
            time.sleep(1)

    except Exception as e:
        print("Error general:", e)
        time.sleep(5)
        machine.reset()  # Reinicia el microcontrolador en caso de fallo grave

# ===== EJECUCIÓN =====
if __name__ == "__main__":
    main()