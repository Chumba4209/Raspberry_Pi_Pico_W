import network
import urequests
import time
import machine
import dht

WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"

THINGSPEAK_API_KEY = "YOUR_API_KEY"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

dht_pin = machine.Pin(4)   # GPIO4 (D2 on NodeMCU, adjust as needed)
sensor = dht.DHT11(dht_pin)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected:", wlan.ifconfig())
    return wlan

def upload_data(temp, hum):
    url = "{}?api_key={}&field1={:.2f}&field2={:.2f}".format(
        THINGSPEAK_URL, THINGSPEAK_API_KEY, temp, hum
    )
    try:
        response = urequests.get(url)
        print("ThingSpeak response:", response.text)
        response.close()
    except Exception as e:
        print("Upload failed:", e)

wlan = connect_wifi()

while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        
        print("Temp: {:.2f} °C, Humidity: {:.2f} %".format(temperature, humidity))
        
        upload_data(temperature, humidity)
    except Exception as e:
        print("Sensor error:", e)
    
    time.sleep(15)  # ThingSpeak requires at least 15s delay
