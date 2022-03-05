import pygame
from resources_manager import *
import miSprite

QUIETO = 0
IZQUIERDA = 1
DERECHA = 2

IDLE = 0
ANDANDO = 1
AGACHADO = 2 # sin usar
ATACANDO = 3

RETARDO_ANIMACION_JUGADOR = [50, 25, 0, 100] # updates que durará cada imagen del personaje
# hay un valor para cada postura: el primero apra idle, el segundo para andar, etc.

#==============================================================================
# Clase Player

class Player(miSprite.MiSprite):
    def __init__(self, pos, groups, obstacle_sprites, image_file, coordeanada_file):
        super().__init__(groups, image_file)

        # Leemos las coordenadas de un archivo de texto
        datos = ResourcesManager.CargarArchivoCoordenadas(coordeanada_file)
        datos = datos.split()
        self.numPostura = IDLE # postura idle
        self.numImagenPostura = 0
        cont = 0
        numImagenes = [2, 2, 2, 2, 3, 5, 3]
        self.coordenadasHoja = []
        for linea in range(0, 7):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        self.rect = pygame.Rect(pos[0],pos[1],self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0

        # El movimiento que esta realizando
        self.movimiento = QUIETO

        # Lado hacia el que esta mirando
        self.mirando = DERECHA

        self.direction = pygame.math.Vector2() # [x:0, y:0]
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        # movimiento
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.mirando = DERECHA
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.mirando = IZQUIERDA
        else:
            self.direction.x = 0

        self.numPostura = IDLE if self.direction.x == 0 and self.direction.y == 0 else ANDANDO

        # ataque
        if keys[pygame.K_SPACE]:
            self.numPostura = ATACANDO # postura atacando
            print("Ataque")
            # falta controlar el COOLDOWN del ataque

    '''
    Este metodo move recibe un parametro speed y no usar self.speed ya que posteriormente lo eliminará de esta clase.

    La idea entonces sería tener una super clase con este metodo, y que tanto los enemigos como el jugador
    hereden de esta clase.
    '''

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() # devuelve un vector con la misma direccion pero con magnitud 1
        
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

    def get_image(self):
        self.actualizarPostura()
        if self.mirando == DERECHA:
            return self.image.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
        elif self.mirando == IZQUIERDA:
            return pygame.transform.flip(self.image.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = RETARDO_ANIMACION_JUGADOR[self.numPostura]
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1

    def update(self):
        self.input()
        self.move(self.speed)