import pygame
from resources_manager import *

# -------------------------------------------------
# Clase Player
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = ResourcesManager.LoadImage("player.png")
        self.rect = self.image.get_rect(topleft = pos)