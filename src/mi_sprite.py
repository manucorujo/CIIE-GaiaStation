import pygame
from resources_manager import *

# -------------------------------------------------
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self, groups, image_file):
        super().__init__(groups)
        self.image = ResourcesManager.LoadSprite(image_file, -1)

    def get_image(self):
        return self.image

    def update(self):
        pass