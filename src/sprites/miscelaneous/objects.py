import sprites.mi_sprite as mi_sprite
from utils.resources_manager import *
import configparser
import pygame

class HeartObject(mi_sprite.MiSprite):
    def __init__(self, pos, groups, image_file, colorkey=-1):
        super().__init__(groups, image_file, colorkey)

        self.parser = configparser.ConfigParser()
        self.parser.read("GaiaStation.config")

        self.rect = self.image.get_rect(topleft = pos)
        self.heal_value = int(self.parser.get("object", "HEART_HEAL_VALUE"))

    
    def get_heal_value(self):
        return self.heal_value


    def get_image(self):
        return self.image

        