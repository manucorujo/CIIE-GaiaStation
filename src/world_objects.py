import pygame
import mi_sprite
from pygame.locals import *
from resources_manager import *

#==============================================================================
# Clase Wall

class Wall(mi_sprite.MiSprite):
    def __init__(self, pos, groups, image_file):
        super().__init__(groups, image_file)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -12)

    def get_image(self):
        return self.image