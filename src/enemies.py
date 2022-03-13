from resources_manager import *
import dinamic_sprites
import pygame

# -------------------------------------------------

class Enemy(dinamic_sprites.DinamicSprite):

    def __init__(self, player, groups, obstacle_sprites, image_file):
        super().__init__(groups, obstacle_sprites, image_file)

        self.player = player

        return

    
    def move_ai(self, speed):
        pass