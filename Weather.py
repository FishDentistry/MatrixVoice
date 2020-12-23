import requests
import json
import pygame
pygame.mixer.init()

class Weather:
    def __init__(self,precipitation,temperature):
        self.precipitation = precipitation
        self.temperature = temperature

    def playPrecipitationSound(self):
        precipitation = self.precipitation
        pygame.mixer.music.load("WeatherSounds/"+precipitation+".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue


    def sayTemperature(self):
        temp = str(self.temperature)
        pygame.mixer.music.load("TemperatureSounds/"+temp[0]+".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        pygame.mixer.music.load("TemperatureSounds/"+temp[1]+".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue



