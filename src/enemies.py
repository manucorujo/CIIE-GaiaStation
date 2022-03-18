from resources_manager import *
import dynamic_sprites

# -------------------------------------------------

class Enemy(dynamic_sprites.DynamicSprite):

    def __init__(self, player, groups, collision_groups, image_file):
        super().__init__(groups, collision_groups, image_file)

        self.player = player

        return

    
    def move_ai(self, speed):
        pass