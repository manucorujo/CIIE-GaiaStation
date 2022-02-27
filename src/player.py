import pygame
from resources_manager import *

#==============================================================================
# Clase Player

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = ResourcesManager.LoadImage("player.png")
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2() # [x:0, y:0]
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    '''
    Este metodo move recibe un parametro speed y no usar self.speed ya que posteriormente lo eliminará de esta clase.

    La idea entonces sería tener una super clase con este metodo, y que tanto los enemigos como el jugador
    hereden de esta clase.
    '''

    def move(self, speed):
        '''
            self.direction tiene que estar normalizado, para no ir más rápido en diagonal
        '''
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() # returns a vector with the same direction but length 1.
        
        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # nos movemos a la derecha
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # hacia abajo
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0: 
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)