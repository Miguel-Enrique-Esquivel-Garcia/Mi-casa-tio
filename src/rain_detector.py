import time
from machine import Pin, PWM

# Rain detector
rain = Pin(4, Pin.IN) # 0 (lots of water) y 4095 (no water)

# Servo
servo = PWM(Pin(13), freq=50)

# Servo angles
Open_angle = 0       # Window open
Closed_angle = 180    # Window closed

def move_servo(angle):
    duty = int((angle / 180 * 75) + 40)
    servo.duty(duty)
"""
180 normalizes the angle to a value between 0 and 1
75 servo movement range in MicroPython
40 minimum servo position
"""

print("Automatic window system")

while True:
    state = rain.value() 

    if state == 0: 
        print("It's raining, window closed")
        move_servo(Closed_angle)

    else: 
        print("Without rain, window open")
        move_servo(Open_angle)

    time.sleep(1)

