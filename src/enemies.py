from resources_manager import *
import dynamic_sprites

# -------------------------------------------------

class Enemy(dynamic_sprites.DynamicSprites):

    def __init__(self, player, groups, collision_groups, image_file, coordeanada_file, num_frames_per_pose, animation_transition_time, speed, health):
        super().__init__(groups, collision_groups, image_file, coordeanada_file, num_frames_per_pose, animation_transition_time)

        self.player = player
        self.speed = speed
        self.health = health

        return

    
    def move_ai(self, speed):
        pass