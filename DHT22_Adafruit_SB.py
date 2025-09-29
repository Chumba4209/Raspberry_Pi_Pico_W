import network
import time
import machine
import random
from umqtt.simple import MQTTClient
import dht
from machine import Pin, SoftI2C
import ssd1306

#Main WiFi Credentials
WIFI_SSID = " "
WIFI_PASSWORD = ""

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

#Main I2C + OLED Setup
i2c = SoftI2C(scl=Pin(21), sda=Pin(20))
oled_width = 128
oled_height = 64
print("I2C Scan: ", i2c.scan())
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

#Main DHT22 Sensor Setup
sensor = dht.DHT22(Pin(2))

#Main MQTT / Adafruit IO Setup
mqtt_server = 'io.adafruit.com'
mqtt_port = 1883
mqtt_user = ''       #Main Your Adafruit username
mqtt_password = ''   #Main Your Adafruit AIO Key

mqtt_topic_temp = 'Chumba4209/feeds/Temperature'
mqtt_topic_hum = 'Chumba4209/feeds/Humidity'

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

#Main Try to Connect to MQTT Broker
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

#Main Program Execution
while True:
    try:
        #Main Read Data from Sensor
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        print("Temp:", temperature, "C")
        print("Humidity:", humidity, "%")

        #Main Display Data on OLED
        oled.fill(0)
        oled.text("DHT SENSOR DATA", 0, 0)
        oled.text('Temp: ' + str(temperature) + " C", 0, 20)
        oled.text('Hum:  ' + str(humidity) + "%", 0, 35)
        oled.show()

        #Main Publish Data to Adafruit IO
        client.publish(mqtt_topic_temp, str(temperature))
        client.publish(mqtt_topic_hum, str(humidity))
        print("Data sent to Adafruit IO")

    except OSError as e:
        print("Failed to read sensor:", e)

    time.sleep(10)   
