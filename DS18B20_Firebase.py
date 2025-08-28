import network
import time
import urequests
import machine
import onewire
import ds18x20

WIFI_SSID = " "
WIFI_PASSWORD = " "

FIREBASE_URL = " "
FIREBASE_SECRET = " "

datapin = machine.Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(datapin))
roms = ds_sensor.scan()

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
    print("Connected! IP:", wlan.ifconfig()[0])

def send_to_firebase(temp):
    url = "{}DS18B20.json?auth={}".format(FIREBASE_URL, FIREBASE_SECRET)
    data = {"Temperature": temp}
    try:
        response = urequests.patch(url, json=data)
        print("Data sent:", data)
        response.close()
    except Exception as e:
        print("Error sending to Firebase:", e)

connect_wifi()

while True:
    try:
        ds_sensor.convert_temp()
        time.sleep_ms(750)
        for rom in roms:
            temp = ds_sensor.read_temp(rom)
            print("Temperature:", temp, "°C")
            send_to_firebase(temp)
    except Exception as e:
        print("Sensor error:", e)
    time.sleep(10)
