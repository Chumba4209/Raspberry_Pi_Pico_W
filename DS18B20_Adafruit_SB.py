import network
import time
import machine
import onewire
import ds18x20
import ssd1306
from umqtt.simple import MQTTClient

#Main WiFi Credentials
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

#Main Adafruit IO Credentials
AIO_USERNAME = "YOUR_ADAFRUIT_USERNAME"
AIO_KEY = "YOUR_ADAFRUIT_IO_KEY"
AIO_FEED = AIO_USERNAME + "/feeds/ds18b20-temp"

#Main WiFi Connection Function
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected to WiFi:", wlan.ifconfig())

#Main Connect to WiFi
connect_wifi()

#Main MQTT Client Setup
client = MQTTClient("ds18b20_client", "io.adafruit.com", 1883, AIO_USERNAME, AIO_KEY)
client.connect()
print("Connected to Adafruit IO")

#Main OLED Setup
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#Main DS18B20 Setup
datapin = machine.Pin(2)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(datapin))
roms = ds_sensor.scan()
print("Found DS18B20 device(s):", roms)

#Main Program Loop
while True:
    #Main Trigger Sensor Conversion
    ds_sensor.convert_temp()
    time.sleep_ms(750)  # wait for sensor conversion

    #Main Read Each Connected DS18B20
    for rom in roms:
        temp = ds_sensor.read_temp(rom)
        print("Temperature:", temp, "°C")

        #Main Publish Data to Adafruit IO
        client.publish(AIO_FEED, str(temp))
        print("Sent to Adafruit:", temp)

        #Main Display on OLED
        oled.fill(0)
        oled.text("DS18B20 Sensor", 5, 10)
        oled.text("Temp: {:.2f} C".format(temp), 5, 30)
        oled.show()

    time.sleep(5)   
