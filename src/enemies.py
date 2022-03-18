from resources_manager import *
import dinamic_sprites

# -------------------------------------------------

class Enemy(dinamic_sprites.DinamicSprite):

    def __init__(self, player, groups, collision_groups, image_file, coordeanada_file, num_frames_per_pose, animation_transition_time):
        super().__init__(groups, collision_groups, image_file, coordeanada_file, num_frames_per_pose, animation_transition_time)

        self.player = player

        return

    
    def move_ai(self, speed):
        pass