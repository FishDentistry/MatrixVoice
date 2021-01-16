import requests
import json
import pygame
pygame.mixer.init()

class Weather:
    #def __init__(self,precipitation,temperature):
        #self.precipitation = precipitation
        #self.temperature = temperature

    #def playPrecipitationSound(self):
        #precipitation = self.precipitation
        #pygame.mixer.music.load("WeatherSounds/"+precipitation+".mp3")
        #pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy() == True:
            #continue


    #def sayTemperature(self):
        #temp = str(self.temperature)
        #pygame.mixer.music.load("TemperatureSounds/"+temp[0]+".mp3")
        #pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy() == True:
            #continue
        #pygame.mixer.music.load("TemperatureSounds/"+temp[1]+".mp3")
        #pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy() == True:
            #continue
    def displayWeather(self):
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Flemingsburg&appid=ac82ae9e71d61ae8a6335898730be24b&units=imperial')
        data = r.json()
        precip = data["weather"][0]['main']
        temp = str(data['main']['temp'])

        pygame.mixer.music.load("WeatherSounds/"+precip+".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        pygame.mixer.music.load("TemperatureSounds/"+temp[0]+".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        pygame.mixer.music.load("TemperatureSounds/"+temp[1]+".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        return precip,temp



