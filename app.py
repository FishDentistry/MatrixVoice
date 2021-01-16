import websocket
import requests
import json
from matrix_lite import led
import time
import servotest2
from Bot import Bot
from threading import Timer
import paho.mqtt.client as mqtt

lightservopin = 0
lightson = True

mytimer = 0
alarmtimer = 0
mybot = Bot()

def on_connect(client,userdata,flags,rc):
    print("Connected to broker")
    client.publish(mqtt_topic,"Operational")
def on_get(client,userdata,msg):
    print("Got msg")
def on_disconnect():
    print("Reconnecting")
    client.connect(mqtt_ip,1883)

mqtt_username = "porcupine"
mqtt_password = "pigs123"
mqtt_topic = "Blinds"
mqtt_ip = "192.168.50.236"
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_get
client.on_disconnect = on_disconnect
client.username_pw_set(mqtt_username,mqtt_password)
client.connect(mqtt_ip,1883)


servotest2.send_servo_command(0,0)
#servotest2.send_servo_command(0,180)
#mytimer = Timer(TIME_TO_OFF,mybot.timerOff)
mybot.displayDefault()


def say(text):
    url = "http://localhost:12101/api/text-to-speech"
    requests.post(url, text)

# Intents are passed through here
def on_message(ws, message):
    global lightson
    global mytimer
    global alarmtimer
    data = json.loads(message)
    #print("**Captured New Intent**")
    #print(data)

    if ("Lights" == data["intent"]["name"]):
        #led.set(data["slots"]["color"])
        #say("Yes")
        if (lightson == True):
            servotest2.send_servo_command(0,120)
            lightson = False
        else:
            servotest2.send_servo_command(0,0)
            lightson = True
    elif ("Weather" == data["intent"]["name"]):
        mybot.giveWeather()
        #client.publish(mqtt_topic,"test")
    elif ("Alarm" == data["intent"]["name"]):
        if not mybot.ALARM_SET:
            time_set = data["tokens"][4]
            total = mybot.setAlarm(time_set)
            mybot.ALARM_SET = True
            mybot.displayDefault()
            alarmtimer = Timer(total,mybot.alarmOff)
            alarmtimer.start()
        else:
            print("Alarm already set")
    elif("Timer" == data["intent"]["name"]):
        mins = data["slots"]["minutes"]
        secs = data["slots"]["seconds"]
        print(mins)
        print(secs)
        total = (mins*60) + secs
        if not mybot.TIMER_SET:
            mytimer = Timer(total,mybot.timerOff)
            mytimer.start()
            mybot.TIMER_SET = True
            mybot.displayDefault()
        else:
            print("Timer already started")
            #mytimer.cancel()
            #mybot.TIMER_SET = False
        #mybot.setCountdown(mins,secs)
    elif ("Cancel" == data["intent"]["name"]):
        if mybot.ALARM_SET:
            alarmtimer.cancel()
            print("Alarm cancelled")
            mybot.displayDefault()
        if mybot.TIMER_SET:
            mytimer.cancel()
            print("Timer cancelled")
            mybot.displayDefault()
        else:
            print("Nothing to cancel")
            mybot.displayDefault()
    elif("Blinds" == data["intent"]["name"]):
        client.publish(mqtt_topic,"Hit blinds")
        mybot.displayDefault()


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("\n**Disconnected**\n")

def on_open(ws):
    print("\n**Connected**\n")

# Start web socket client
if __name__ == "__main__":
    client.loop_start()
    ws = websocket.WebSocketApp("ws://localhost:12101/api/events/intent",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()