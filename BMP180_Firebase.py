import network
import urequests
import time
from machine import I2C, Pin
import bmp180

WIFI_SSID = "Lukrasta"
WIFI_PASS = "Cycy12345"

API_KEY = "AIzaSyCbyeMEQ5g8UpT8PoEYdQ5ODUdI-vi55YU"
PROJECT_ID = "bmp180-firestore"
USER_EMAIL = "cybrin101@gmail.com"
USER_PASSWORD = "Sacho3280."

# Firestore document path
DOCUMENT_PATH = "EspData/BMP180"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected, IP:", wlan.ifconfig()[0])
    return wlan

def get_token():
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}".format(API_KEY)
    payload = {
        "email": USER_EMAIL,
        "password": USER_PASSWORD,
        "returnSecureToken": True
    }
    headers = {"Content-Type": "application/json"}
    response = urequests.post(url, json=payload, headers=headers)
    data = response.json()
    response.close()
    return data.get("idToken", None)

def send_to_firestore(id_token, temperature, pressure):
    url = "https://firestore.googleapis.com/v1/projects/{}/databases/(default)/documents/{}".format(PROJECT_ID, DOCUMENT_PATH)
    headers = {
        "Authorization": "Bearer {}".format(id_token),
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "Temperature": {"stringValue": str(round(temperature, 2))},
            "Pressure": {"stringValue": str(round(pressure, 2))}
        }
    }
    response = urequests.patch(url, json=payload, headers=headers)
    print("Firestore response:", response.text)
    response.close()

i2c = I2C(scl=Pin(22), sda=Pin(21))  # ESP32 default pins
sensor = bmp180.BMP180(i2c)
sensor.oversample_sett = 2
sensor.baseline = 101325

wlan = connect_wifi()
id_token = get_token()

while True:
    try:
        temp = sensor.temperature - 170  # adjust offset like in Arduino code
        pressure = (sensor.pressure / 100) - 300

        print("Temperature:", temp, "C")
        print("Pressure:", pressure, "hPa")

        if id_token:
            send_to_firestore(id_token, temp, pressure)
        else:
            print("No Firebase token!")

    except Exception as e:
        print("Error:", e)

    time.sleep(10)
