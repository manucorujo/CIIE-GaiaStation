import configparser
from resources_manager import *
import dinamic_sprites
import pygame

# -------------------------------------------------
# Lectura do ficheiro de configuración

ANIMATION_TRANSITION_TIME = 7
NUM_FRAMES_PER_POSE = [3]

'''parser = configparser.ConfigParser()
parser.read("GaiaStation.config")
ANIMATION_TRANSITION_TIME = int(parser.get("bullets", "RETARDO_ANIMACION_BALA"))'''

# -------------------------------------------------

class Projectile(dinamic_sprites.DinamicSprite):
    def __init__(self, player, groups, collision_groups, image_file, coordeanada_file, borrar_ataque):
        super().__init__(groups, collision_groups, image_file, coordeanada_file, NUM_FRAMES_PER_POSE, ANIMATION_TRANSITION_TIME)

        self.orientation = player.get_attackOrientation()
        self.current_pose_frame = 0

        self.animation_delay = ANIMATION_TRANSITION_TIME
        self.speed = 3

        self.borrar_ataque = borrar_ataque

        # Grupos para colisions
        self.obstacle_sprites = collision_groups[0]
        self.enemies_sprites = collision_groups[1]
        
        # placement
        aux_img = self.get_image() # para que se cargue el rect de la imagen
        if self.orientation == dinamic_sprites.RIGHT: 
            self.rect = aux_img.get_rect(midleft = player.rect.midright)
        elif self.orientation == dinamic_sprites.LEFT:
            self.rect = aux_img.get_rect(midright = player.rect.midleft) 
        elif self.orientation == dinamic_sprites.UP:
            self.rect = aux_img.get_rect(midbottom = player.rect.midtop)
        elif self.orientation == dinamic_sprites.DOWN:
            self.rect = aux_img.get_rect(midtop = player.rect.midbottom) 


    def move(self, speed):
        if self.orientation == dinamic_sprites.RIGHT:
            self.rect.x += speed
        elif self.orientation == dinamic_sprites.LEFT:
            self.rect.x -= speed
        elif self.orientation == dinamic_sprites.UP:
            self.rect.y -= speed
        elif self.orientation == dinamic_sprites.DOWN:
            self.rect.y += speed
        self.collision(self.orientation)


    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.rect):
                self.borrar_ataque()

        enemy_hitted = pygame.sprite.spritecollideany(self, self.enemies_sprites)
        if enemy_hitted and not enemy_hitted.is_death:
            enemy_hitted.take_damage(1)
            self.borrar_ataque()


    def get_image(self):
        self.update_pose()
        return self.image.subsurface(self.coordinates_sheet[0][self.current_pose_frame])


    def update_pose(self):
        if self.current_pose_frame >= len(self.coordinates_sheet[0])-1:
            return
        self.animation_delay -= 1
        # Miramos si ha pasado el retardo
        if (self.animation_delay < 0):
            self.animation_delay = ANIMATION_TRANSITION_TIME
            # Si ha pasado, actualizamos la postura
            self.current_pose_frame += 1
        
    def update(self):
        self.move(self.speed)
