import machine
import time

BUTTON_PIN = 7   
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

def is_long_press(pin, duration=1000):
    press_time = time.ticks_ms()
    while pin.value() == 0:   # 0 = pressed (since pull-up is used)
        if time.ticks_diff(time.ticks_ms(), press_time) > duration:
            return True
    return False

while True:
    if button.value() == 0:   # Button pressed
        if is_long_press(button):
            print("Long pressed")
            time.sleep(0.5)
        else:
            print("Switch pushed")
            time.sleep(1)
    else:
        print("Switch released")
        time.sleep(0.5)
