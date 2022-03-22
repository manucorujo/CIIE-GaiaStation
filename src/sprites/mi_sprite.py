import pygame
from utils.resources_manager import *

# -------------------------------------------------
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self, groups, image_file, colorkey=-1):
        super().__init__(groups)
        self.image = ResourcesManager.LoadSprite(image_file, colorkey)

    def get_image(self):
        return self.image

    def update(self):
        pass