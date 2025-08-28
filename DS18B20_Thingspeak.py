import network
import urequests
import time
import machine
import onewire
import ds18x20

WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"

THINGSPEAK_API_KEY = "YOUR_API_KEY"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

ds_pin = machine.Pin(4)   # GPIO4 (D2 on NodeMCU, adjust as needed)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print("Found DS18B20 devices:", roms)

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

def upload_data(temp):
    url = "{}?api_key={}&field1={:.2f}".format(
        THINGSPEAK_URL, THINGSPEAK_API_KEY, temp
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
        ds_sensor.convert_temp()
        time.sleep_ms(750)   # Wait for conversion
        for rom in roms:
            temperature = ds_sensor.read_temp(rom)
            print("Temperature: {:.2f} °C".format(temperature))
            upload_data(temperature)
    except Exception as e:
        print("Sensor error:", e)
    
    time.sleep(15)  # ThingSpeak minimum interval
