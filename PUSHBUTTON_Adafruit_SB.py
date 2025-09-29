import network
import time
import machine
import ssd1306
from umqtt.simple import MQTTClient

#Main WiFi Credentials
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"

#Main Adafruit IO Credentials
AIO_USERNAME = "YOUR_ADAFRUIT_IO_USERNAME"
AIO_KEY = "YOUR_ADAFRUIT_IO_KEY"
AIO_FEED = AIO_USERNAME + "/feeds/button"

#Main Pin Setup
BUTTON_PIN = 7    # Adjust for your board
SCL_PIN = 10
SDA_PIN = 8

#Main Button Initialization
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

#Main OLED Setup
i2c = machine.I2C(0, scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#Main OLED Message Function
def show_message(line1, line2):
    oled.fill(0)
    oled.text(line1, 20, 30)
    oled.text(line2, 20, 45)
    oled.show()

#Main Long Press Detection
def is_long_press(pin, duration=1000):
    press_time = time.ticks_ms()
    while pin.value() == 0:
        if time.ticks_diff(time.ticks_ms(), press_time) > duration:
            return True
    return False

#Main WiFi Connection
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        show_message("WiFi", "Connecting...")
        time.sleep(0.5)
    show_message("WiFi", "Connected")
    return wlan

#Main MQTT Connection
def connect_mqtt():
    client = MQTTClient("buttonClient", "io.adafruit.com", 0, AIO_USERNAME, AIO_KEY)
    client.connect()
    show_message("MQTT", "Connected")
    return client

#Main Connect WiFi and MQTT
wlan = connect_wifi()
mqtt = connect_mqtt()

#Main Loop
while True:
    if button.value() == 0:  # Pressed
        if is_long_press(button):
            show_message("Long", "pressed")
            mqtt.publish(AIO_FEED.encode(), b"LONG")
            time.sleep(0.5)
        else:
            show_message("Button", "pushed")
            mqtt.publish(AIO_FEED.encode(), b"PUSHED")
            time.sleep(1)
    else:
        show_message("Button", "released")
        mqtt.publish(AIO_FEED.encode(), b"RELEASED")
        time.sleep(0.5)
