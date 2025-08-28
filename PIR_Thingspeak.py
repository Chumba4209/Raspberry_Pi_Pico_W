import network
import urequests
import time
import machine

WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"

THINGSPEAK_API_KEY = "YOUR_API_KEY"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

pir_pin = machine.Pin(14, machine.Pin.IN) 
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

def upload_data(motion_detected):
    url = "{}?api_key={}&field1={}".format(
        THINGSPEAK_URL, THINGSPEAK_API_KEY, motion_detected
    )
    try:
        response = urequests.get(url)
        print("ThingSpeak response:", response.text)
        response.close()
    except Exception as e:
        print("Upload failed:", e)

wlan = connect_wifi()

while True:
    motion = pir_pin.value()  # 1 = motion detected, 0 = no motion
    print("Motion Detected:" if motion else "No Motion")
    upload_data(motion)
    time.sleep(15) 
