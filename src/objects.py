import configparser
from resources_manager import *
import mi_sprite
import pygame

# -------------------------------------------------

#TODO: Hay que sacar esto y hacer el config singleton
HEART_HEAL_VALUE = 1

class HeartObject(mi_sprite.MiSprite):
    def __init__(self, pos, groups, image_file, colorkey=-1):
        super().__init__(groups, image_file, colorkey)

        self.rect = self.image.get_rect(topleft = pos)
        self.heal_value = HEART_HEAL_VALUE

    
    def get_heal_value(self):
        return self.heal_value


    def get_image(self):
        return self.image

        