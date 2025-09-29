import network
import time
import machine
import random
from umqtt.simple import MQTTClient
from machine import Pin, SoftI2C
import ssd1306

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

#Main OLED Setup
i2c = SoftI2C(scl=Pin(21), sda=Pin(20))  
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

#Main PIR Sensor Setup
PIR_PIN = 7   # Adjust GPIO based on your wiring
pir = Pin(PIR_PIN, Pin.IN)

#Main Adafruit IO Credentials
mqtt_server = 'io.adafruit.com'
mqtt_port = 1883
mqtt_user = ' '    # Your Adafruit username
mqtt_password = ' '  # Your AIO Key

mqtt_topic_pir = 'Chumba4209/feeds/PIR'  #Main PIR Feed in Adafruit IO
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

#Main MQTT Connect
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

#Main Program Loop
while True:
    try:
        #Main Read PIR Value
        motionDetected = pir.value()   # 1 if motion detected, 0 if not

        #Main Display on OLED
        oled.fill(0)
        oled.text("PIR SENSOR", 25, 0)
        
        if motionDetected == 1:
            oled.text("Motion", 30, 25)
            oled.text("Detected!", 25, 40)
            print("Motion Detected!")
            client.publish(mqtt_topic_pir, "1")   #Main Publish 1 to Adafruit
        else:
            oled.text("No Motion", 25, 25)
            oled.text("Detected", 30, 40)
            print("No Motion")
            client.publish(mqtt_topic_pir, "0")   #Main Publish 0 to Adafruit
        
        oled.show()
        time.sleep(5)   #Main Delay Between Checks

    except OSError as e:
        print("Sensor or MQTT error:", e)
        reconnect()
