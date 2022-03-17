import pygame
from mi_sprite import *
from pygame.locals import *
from resources_manager import *

#==============================================================================
# Clase Obstacle

class Obstacle(MiSprite):
    def __init__(self, pos, groups, image_file, colorkey=-1):
        super().__init__(groups, image_file, colorkey)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -6)

    def get_image(self):
        return self.image