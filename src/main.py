"""
Complete unified system:
- MQ-2 activates buzzer and relay (fan) if the temperature exceeds 550°C.
- Rain sensor controls the servo to open/close the window.
- DHT11 activates the same relay when the temperature exceeds 25°C.
"""

from machine import Pin, ADC, PWM
import utime
import dht

# ======================================================================
# ----------------------------  MQ-2  ----------------------------------
# ======================================================================

AO_PIN = ADC(Pin(36))            
AO_PIN.width(ADC.WIDTH_12BIT)
AO_PIN.atten(ADC.ATTN_11DB)

buzzer = Pin(15, Pin.OUT)        
relay = Pin(5, Pin.OUT)          # <-- RELAY = FAN

buzzer.value(0)
relay.value(0)

# ======================================================================
# ---------------------  SENSOR DE LLUVIA + SERVO  ---------------------
# ======================================================================

rain = Pin(4, Pin.IN)

servo = PWM(Pin(13), freq=50)

OPEN_ANGLE = 0
CLOSED_ANGLE = 90

def move_servo(angle):
    duty = int((angle / 180 * 75) + 40)
    servo.duty(duty)

# ======================================================================
# -----------------------------  DHT11  --------------------------------
# ======================================================================

sensor = dht.DHT11(Pin(14))

TEMP_MAX = 30

# ======================================================================
# ---------------------------  MAIN LOOP  ------------------------------
# ======================================================================

print("🌡🌧🔥 SYSTEM ONLINE — MULTI-SENSOR CONTROL")

while True:

    # ---------------- MQ-2 GAS SENSOR ----------------
    gas_value = AO_PIN.read()
    print("MQ-2 Value:", gas_value)

    if gas_value > 550:
        print("⚠ High GAS — Alarm + Ventilator ON")
        buzzer.value(1)
        relay.value(1)  # <-- ¿same relay 
    else:
        buzzer.value(0)

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
            relay.value(1)     # <-- same relay for ventilator
        else:
            print("❄ Normal temp")
            # Turn off the relay ONLY if MQ-2 did not activate it
            if gas_value <= 550:
                relay.value(0)

    except OSError as e:
        print("❌ ERROR DHT11:", e)

    print("-----------------------------------")
    utime.sleep(1)