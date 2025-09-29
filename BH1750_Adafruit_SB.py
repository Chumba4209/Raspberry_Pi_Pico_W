import network
import time
import machine
import random
from umqtt.simple import MQTTClient
from machine import Pin, SoftI2C
import ssd1306
import bh1750   #Ensure bh1750.py is in the lib/ folder

#Main WiFi Credentials
WIFI_SSID = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

#Main WiFi Connection Function
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
            print("Trying to connect...")
    print("Connected to WiFi:", wlan.ifconfig())

#Main Connect to WiFi
connect_wifi()

#Main I2C and OLED Setup
i2c = SoftI2C(scl=Pin(21), sda=Pin(20))
print("I2C devices found:", i2c.scan())

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

#Main Sensor Setup (BH1750)
sensor = bh1750.BH1750(i2c)

#Main MQTT / Adafruit IO Setup
mqtt_server = 'io.adafruit.com'
mqtt_port = 1883
mqtt_user = ''        #Main Your Adafruit username
mqtt_password = ''    #Main Your Adafruit AIO Key
mqtt_topic_lux = 'Chumba4209/feeds/Light'  #Main Create this feed in Adafruit IO
mqtt_client_id = str(random.randint(10000, 999999))

#Main MQTT Connection Function
def mqtt_connect():
    client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_server,
        port=mqtt_port,
        user=mqtt_user,
        password=mqtt_password,
        keepalive=3600
    )
    client.connect()
    print('Connected to %s MQTT Broker' % (mqtt_server))
    return client

#Main Reconnect Function
def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

#Main Try to Connect to Adafruit IO
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

#Main Program Execution
while True:
    try:
        #Main Read Sensor Data
        lux = sensor.luminance(bh1750.BH1750.CONT_HIRES_1)
        print("Light Level:", lux, "lx")

        #Main Display on OLED
        oled.fill(0)
        oled.text("BH1750 SENSOR", 15, 0)
        oled.text("Light:", 20, 25)
        oled.text(str(round(lux, 2)) + " lx", 20, 40)
        oled.show()

        #Main Publish Data to Adafruit IO
        client.publish(mqtt_topic_lux, str(round(lux, 2)))
        print("Data sent to Adafruit IO")

    except OSError as e:
        print("Sensor or MQTT error:", e)
        reconnect()

    time.sleep(10)   
