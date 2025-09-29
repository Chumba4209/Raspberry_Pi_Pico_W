#Main BMP180 with WiFiManager + Firestore
import network
import urequests
import time
from machine import I2C, Pin
import bmp180
import wifi_manager   

# Firestore config 
API_KEY = "YOUR_API_KEY"
PROJECT_ID = "your-project-id"
USER_EMAIL = "your-email@example.com"
USER_PASSWORD = "your-password"
DOCUMENT_PATH = "EspData/BMP180"

#Main Setup BMP180 sensor
i2c = I2C(scl=Pin(22), sda=Pin(21))  # ESP32 default pins
sensor = bmp180.BMP180(i2c)
sensor.oversample_sett = 2
sensor.baseline = 101325

#Main Connect WiFi with WiFiManager
print("Starting WiFiManager...")
wlan, config = wifi_manager.connect()   # Opens portal if no saved credentials

#Main Authentication function
def get_token():
    api_key = config.get("api_key", API_KEY)
    email = config.get("user_email", USER_EMAIL)
    password = config.get("user_password", USER_PASSWORD)

    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}".format(api_key)
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = urequests.post(url, json=payload, headers=headers)
        data = response.json()
        response.close()
        return data.get("idToken", None)
    except Exception as e:
        print("Error getting token:", e)
        return None

#Main Firestore send function
def send_to_firestore(id_token, temperature, pressure):
    project_id = config.get("project_id", PROJECT_ID)
    document_path = config.get("document_path", DOCUMENT_PATH)

    url = "https://firestore.googleapis.com/v1/projects/{}/databases/(default)/documents/{}".format(project_id, document_path)
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
    try:
        response = urequests.patch(url, json=payload, headers=headers)
        print("Firestore response:", response.text)
        response.close()
    except Exception as e:
        print("Error sending to Firestore:", e)

#Main Get ID token
id_token = get_token()

#Main Loop
while True:
    try:
        temp = sensor.temperature - 170  # offset (adjust if needed)
        pressure = (sensor.pressure / 100) - 300

        print("Temperature:", temp, "C")
        print("Pressure:", pressure, "hPa")

        if id_token:
            send_to_firestore(id_token, temp, pressure)
        else:
            print("No Firebase token! Retrying...")
            id_token = get_token()

    except Exception as e:
        print("Error:", e)

    time.sleep(10)
