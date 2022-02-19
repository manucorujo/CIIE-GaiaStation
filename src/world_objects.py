import pygame
from pygame.locals import *
from resources_manager import *

# -------------------------------------------------
# Clase Wall
class Wall(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = ResourcesManager.LoadImage("wall.png")
        self.rect = self.image.get_rect(topleft = pos)