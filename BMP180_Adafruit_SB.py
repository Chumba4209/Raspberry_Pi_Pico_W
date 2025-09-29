import network
import time
import machine
import random
from umqtt.simple import MQTTClient
from machine import Pin, SoftI2C
import ssd1306
from bmp085 import BMP180

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
print("I2C Scan:", i2c.scan())

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

#Main Sensor Setup (BMP180)
bmp = BMP180(i2c)
bmp.oversample = 2
bmp.sealevel = 1010.5   #Main Adjust to your local sea-level pressure

#Main MQTT / Adafruit IO Setup
mqtt_server = 'io.adafruit.com'
mqtt_port = 1883
mqtt_user = ''         #Main Your Adafruit username
mqtt_password = ''     #Main Your Adafruit AIO Key

mqtt_topic_temp = 'Chumba4209/feeds/Temperature'  #Main Update to match your feed name
mqtt_topic_pres = 'Chumba4209/feeds/Pressure'     #Main Update to match your feed name

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
        tempC = bmp.temperature
        pres_hPa = bmp.pressure
        tempF = (tempC * 9/5) + 32

        print("Temp:", tempC, "C")
        print("Temp:", tempF, "F")
        print("Pressure:", pres_hPa, "hPa")

        #Main Display Data on OLED
        oled.fill(0)
        oled.text("BMP180 DATA", 0, 0)
        oled.text("Temp: " + str(round(tempC, 1)) + " C", 0, 16)
        oled.text("Temp: " + str(round(tempF, 1)) + " F", 0, 26)
        oled.text("Pres: " + str(round(pres_hPa, 1)), 0, 36)
        oled.show()

        #Main Publish Data to Adafruit IO
        client.publish(mqtt_topic_temp, str(round(tempC, 1)))
        client.publish(mqtt_topic_pres, str(round(pres_hPa, 1)))
        print("Data sent to Adafruit IO")

    except OSError as e:
        print("Sensor or MQTT error:", e)
        reconnect()

    time.sleep(10)   
