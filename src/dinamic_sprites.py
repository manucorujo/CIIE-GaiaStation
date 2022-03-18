import configparser
from resources_manager import *
import mi_sprite
import pygame
import math

# -------------------------------------------------

# Lectura do ficheiro de configuración
parser = configparser.ConfigParser()
parser.read("GaiaStation.config")
HORIZONTAL = int(parser.get("dinamic_sprites", "HORIZONTAL"))
VERTICAL = int(parser.get("dinamic_sprites", "VERTICAL"))

LEFT = int(parser.get("dinamic_sprites", "LEFT"))
RIGHT = int(parser.get("dinamic_sprites", "RIGHT"))
UP = int(parser.get("dinamic_sprites", "UP"))
DOWN = int(parser.get("dinamic_sprites", "DOWN"))

# -------------------------------------------------

class DinamicSprite(mi_sprite.MiSprite):
    "Los Sprites que tendra este juego"
    def __init__(self, groups, collision_groups, image_file):
        super().__init__(groups, image_file)
    
        self.obstacle_sprites = collision_groups[0]
        self.hitbox = None


    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() # devuelve un vector con la misma direccion pero con magnitud 1
        
        # Uso de round -> el rect (hitbox) funciona con numero enteros, si no usamos round, el rect automaticamente 
        # redondeara a la baja, dando un comportamiento distinto entre valores negativos y positivos

        self.hitbox.x += round(self.direction.x * speed)
        self.collision(HORIZONTAL)
        self.hitbox.y += round(self.direction.y * speed)
        self.collision(VERTICAL)
        self.rect.center = self.hitbox.center # importante mantener el centro del rect

    
    def collision(self, direction):
        if direction == HORIZONTAL:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # nos movemos a la derecha
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == VERTICAL:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # hacia abajo
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: 
                        self.hitbox.top = sprite.hitbox.bottom


    def update_pose(self):
        pass


    def wave_value(self):
        value = math.sin(pygame.time.get_ticks())
        return 255 if value >= 0 else 0
