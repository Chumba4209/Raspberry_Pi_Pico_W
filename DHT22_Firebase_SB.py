import network
import time
import urequests
from machine import Pin
import dht

#Main WiFi Credentials
WIFI_SSID = " "
WIFI_PASSWORD = " "

#Main Firebase Realtime Database Setup
FIREBASE_URL = " "
FIREBASE_SECRET = "YOUR_DATABASE_SECRET"   # From Firebase console -> Project Settings -> Service accounts -> Database secrets

#Main DHT22 Sensor Setup
dht_pin = Pin(4)  
sensor = dht.DHT22(dht_pin)

#Main WiFi Connection Function
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    print("Connecting to WiFi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nConnected! IP:", wlan.ifconfig()[0])

#Main Firebase Send Function
def send_to_firebase(temp, hum):
    url = "{}DHT22.json?auth={}".format(FIREBASE_URL, FIREBASE_SECRET)
    data = {"Temperature": temp, "Humidity": hum}
    try:
        response = urequests.patch(url, json=data)
        print("Data sent:", data)
        response.close()
    except Exception as e:
        print("Error sending to Firebase:", e)

#Main Program Execution
connect_wifi()

while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        print("Temperature: {}°C, Humidity: {}%".format(temperature, humidity))

        send_to_firebase(temperature, humidity)

    except Exception as e:
        print("Sensor error:", e)

    time.sleep(10)   
