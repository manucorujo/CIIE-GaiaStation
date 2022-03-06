import pygame
import miSprite
from pygame.locals import *
from resources_manager import *

#==============================================================================
# Clase Wall

class Wall(miSprite.MiSprite):
    def __init__(self, pos, groups, image_file):
        super().__init__(groups, image_file)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -6)

    def get_image(self):
        return self.image