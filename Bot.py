from Weather import Weather
import PIL.Image
import time
from threading import Timer
import pygame
import datetime

pygame.mixer.init()

class Bot:
    myweather = Weather()
    ASCII_CHARS = ["@","#","S","%","?","*","+",";",":",",","."]
    ALARM_SET = False
    TIMER_SET = False
    mytimer = 0
    mytimerCountdown = 0

    def giveWeather(self):
        precipitation,temp = self.myweather.displayWeather()
        img = PIL.Image.open("WeatherImages/"+precipitation+".png")
        self.displayReaction(img)
        print(temp)
        time.sleep(5)
        for i in range(20):
            print(" ")
        img = PIL.Image.open("ReactionImages/Neutral.jpg")
        self.displayReaction(img)

    def displayReaction(self,image,new_width=50):
        new_image_data = self.convertAscii(self.convertGrayscale(self.resize_image(image)))
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(new_image_data[i:(i+new_width)] for i in range(0,pixel_count,new_width))
        print(ascii_image)

    def displayDefault(self):
        for i in range(20):
            print(" ")
        img = PIL.Image.open("ReactionImages/Neutral.jpg")
        self.displayReaction(img)

    def resize_image(self,image,new_width=50):
        width,height = image.size
        ratio = height / width
        new_height = int(new_width*ratio)
        resized_image = image.resize((new_width,new_height))
        return resized_image

    def convertGrayscale(self,image):
        grayscale_image = image.convert("L")
        return grayscale_image

    def convertAscii(self,image):
        pixels = image.getdata()
        characters = "".join([self.ASCII_CHARS[pixel//25] for pixel in pixels])
        return characters

    def alarmOff(self):
        img = PIL.Image.open("ReactionImages/Bell.png")
        self.displayReaction(img)
        pygame.mixer.music.load("Alarm.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        for i in range(20):
            print(" ")
        self.ALARM_SET = False
        img = PIL.Image.open("ReactionImages/Neutral.jpg")
        self.displayReaction(img)

    def setAlarm(self,time):
        current_time = datetime.datetime.now()
        hour = current_time.hour
        minute = current_time.minute
        second = current_time.second
        till_midnight = ((24 - hour - 1) * 60 * 60) + ((60 - minute - 1) * 60) + (60 -second)
        total_wait = till_midnight + (time*60*60)
        #if not self.ALARM_SET:
            #self.mytimer = Timer(total_wait,self.alarmOff)
            #self.mytimer.start()
            #self.ALARM_SET = True
        #else:
            #self.mytimer.cancel()
            #self.ALARM_SET = False
        return total_wait

    def timerOff(self):
        img = PIL.Image.open("ReactionImages/Bell.png")
        print("Done")
        self.displayReaction(img)
        pygame.mixer.music.load("Timer.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        for i in range(20):
            print(" ")
        img = PIL.Image.open("ReactionImages/Neutral.jpg")
        self.displayReaction(img)
        self.TIMER_SET = False

    #def setCountdown(self,timemins,timesecs):
        #print("Here")
        #if not self.TIMER_SET:
            #total = (timemins*60)+timesecs
            #print(total)
            #mytimer = Timer(5,timerOff)
            #mytimer.start()
            #self.TIMER_SET = True
        #else:
            #self.mytimerCountdown.cancel()
            #self.TIMER_SET = False