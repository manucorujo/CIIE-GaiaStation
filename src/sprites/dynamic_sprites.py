# SPDX-FileCopyrightText: 2024 Manu Corujo <manucorujo@gmail.com>
#
# SPDX-License-Identifier: MIT

import pygame

import sprites.mi_sprite as mi_sprite
from utils.resources_manager import *
from utils.constants import *

# -------------------------------------------------

class DynamicSprites(mi_sprite.MiSprite):
    "Los Sprites que tendra este juego"
    def __init__(self, groups, collision_groups, image_file, coordeanada_file, num_frames_per_pose, animation_transition_time):
        super().__init__(groups, image_file)
    
        self.obstacle_sprites = collision_groups[0]
        self.hitbox = None

        # folla de sprites
        self.num_frames_per_pose = num_frames_per_pose
        self.animation_transition_time = animation_transition_time 
        self.coordinates_sheet = []
        # O retardo a hora de cambiar a imaxe do Sprite, para que non se faga moi rapido
        self.animation_delay = 0

        # Cargamos o arquivo de coordenadas
        datos = ResourcesManager.load_coordinates_file(coordeanada_file)
        datos = datos.split()
        
        # Inicialización dos frames para as animacions
        cont = 0
        for pose in range(len(self.num_frames_per_pose)):
            self.coordinates_sheet.append([])

            for frame in range(self.num_frames_per_pose[pose]):
                self.coordinates_sheet[pose].append( 
                    pygame.Rect(
                        (
                            int(datos[cont]), 
                            int(datos[cont+1])
                        ), 
                        (
                            int(datos[cont+2]), 
                            int(datos[cont+3])
                        )
                    )
                )
                cont += 4



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


    def get_image(self):
        self.update_pose()
        if self.orientation == RIGHT:
            return self.image.subsurface(self.coordinates_sheet[self.current_pose][self.current_pose_frame])
        elif self.orientation == LEFT:
            return pygame.transform.flip(self.image.subsurface(self.coordinates_sheet[self.current_pose][self.current_pose_frame]), 1, 0)


    def update_pose(self):
        if self.direction.x > 0:
            self.orientation = RIGHT
        elif self.direction.x < 0:
            self.orientation = LEFT

        self.animation_delay -= 1

        if (self.animation_delay < 0):
            self.animation_delay = self.animation_transition_time[self.current_pose]
            self.current_pose_frame += 1

            if self.current_pose_frame >= len(self.coordinates_sheet[self.current_pose]):
                self.current_pose_frame = 0

            elif self.current_pose_frame < 0:
                self.current_pose_frame = len(self.coordinates_sheet[self.current_pose])-1
