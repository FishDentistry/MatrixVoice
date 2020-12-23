import websocket
import requests
import json
from matrix_lite import led
import time
import servo
import Weather

lightservopin = 0
lightson = True

servo.send_servo_command(0,0)
#servotest2.send_servo_command(0,180)




def say(text):
    url = "http://localhost:12101/api/text-to-speech"
    requests.post(url, text)

# Intents are passed through here
def on_message(ws, message):
    global lightson
    data = json.loads(message)
    print("**Captured New Intent**")
    print(data)

    if ("Lights" == data["intent"]["name"]):
        #led.set(data["slots"]["color"])
        #say("Yes")
        if (lightson == True):
            servo.send_servo_command(0,180)
            lightson = False
        else:
            servo.send_servo_command(0,0)
            lightson = True
    elif ("Weather" == data["intent"]["name"]):
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Flemingsburg&appid="YOUR_ID_HERE"&units=imperial')
        data = r.json()
        precip = data["weather"][0]['main']
        temp = data['main']['temp']
        currweather = Weather.Weather(precip,temp)
        currweather.playPrecipitationSound()
        currweather.sayTemperature()

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("\n**Disconnected**\n")

def on_open(ws):
    print("\n**Connected**\n")

# Start web socket client
if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://localhost:12101/api/events/intent",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
