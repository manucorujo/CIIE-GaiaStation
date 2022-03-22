from sprites.mi_sprite import *
from pygame.locals import *
from utils.resources_manager import *
import configparser

parser = configparser.ConfigParser()
parser.read("GaiaStation.config")
TILE_SIZE = int(parser.get("level", "TILE_SIZE"))

#==============================================================================
# Clase Obstacle

class Obstacle(MiSprite):
    def __init__(self, pos, groups, image_file, colorkey=-1):
        super().__init__(groups, image_file, colorkey)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -round(TILE_SIZE * 1/3))

    def get_image(self):
        return self.image


#==============================================================================
# Clase Flag

class Flag(pygame.sprite.Sprite):
    def __init__(self, pos, tilesize, groups):
        super().__init__(groups)
        self.rect = Rect(pos, tilesize)
        self.image = pygame.Surface((0, 0))

