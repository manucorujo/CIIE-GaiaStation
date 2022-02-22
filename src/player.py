import pygame
from resources_manager import *

#==============================================================================
# Clase Player

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = ResourcesManager.LoadImage("player.png")
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2() # [x:0, y:0]
        self.speed = 5

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
            self.direction tiene que estar normalizado

            Es decir, si tenemos un vector de dirección [1,1], no puede ir más rápido
            que con [1,0] o [0,1]. De la siguiente manera conseguimos que nunca sea 
            mayor que 1 ¿?
        '''
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * speed

    def update(self):
        self.input()
        self.move(self.speed)