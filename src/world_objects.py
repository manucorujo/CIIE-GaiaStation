import pygame
from pygame.locals import *
from resources_manager import *

#==============================================================================
# Clase Obstacle

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((32, 32))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -12)
