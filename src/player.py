import pygame
from resources_manager import *
import dinamic_sprites

# -------------------------------------------------

IDLE = 0
ANDANDO = 1
AGACHADO = 2 # sin usar
ATACANDO = 3

# esto de al animación y retardos del ataque está completamente abierto a cambios
TIEMPO_ATAQUE = 300
TIEMPO_RECARGA = 600
RETARDO_ANIMACION_ATAQUE = int((60 * int(TIEMPO_ATAQUE / 2))/1000)

# la caurta posicion, ataque, hay que ajustarla y coordinarla
RETARDO_ANIMACION_JUGADOR = [50, 25, 0, RETARDO_ANIMACION_ATAQUE] # updates que durará cada imagen del personaje
# hay un valor para cada postura: el primero para idle, el segundo para andar, etc.

COOLDOWN_DAMAGE_TAKEN = 1500

# -------------------------------------------------

class Player(dinamic_sprites.DinamicSprite):
    def __init__(self, pos, groups, collision_groups, crear_ataque, borrar_ataque, image_file, coordeanada_file):
        super().__init__(groups, collision_groups, image_file)

        # Leemos las coordenadas de un archivo de texto
        datos = ResourcesManager.CargarArchivoCoordenadas(coordeanada_file)
        datos = datos.split()
        self.postura = IDLE # postura idle
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

        # Hitbox: se corresponde al rect del personaje, pero recortando por arriba y por abajo para así tener un comportamiento más realista con las paredes superiores e inferiores
        self.rect = pygame.Rect(pos[0],pos[1],self.coordenadasHoja[self.postura][self.numImagenPostura][2],self.coordenadasHoja[self.postura][self.numImagenPostura][3])
        self.hitbox = self.rect.inflate(0, -12)

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0

        # Orientacion del personaja (der o izq)
        self.orientacion = dinamic_sprites.RIGHT
        self.orientacionAtaque = dinamic_sprites.RIGHT

        # movimiento
        self.direction = pygame.math.Vector2() # [x:0, y:0]

        # cooldowns
        self.is_attacking = False
        self.cooldownAtaque = TIEMPO_ATAQUE
        self.tiempoAtaque = 0

        self.recargando = False
        self.cooldownRecarga = TIEMPO_RECARGA
        self.tiempoRecarga = 0

        self.damage_taken = False
        self.cooldown_damage_taken = COOLDOWN_DAMAGE_TAKEN
        self.damage_taken_time = 0

        # armas
        self.crear_ataque = crear_ataque
        self.borrar_ataque = borrar_ataque

        # Grupos para colisions
        self.obstacle_sprites = collision_groups[0]
        self.enemies_sprites = collision_groups[1]

        # Estadisticas: vida, etc
        self.max_vida = 3 # golpes para morir
        self.vida = self.max_vida 
        self.speed = 3 # velocidad de movimiento


    def input(self):

        if self.is_attacking:
            return

        keys = pygame.key.get_pressed()

        ''' TEST PARA PERDER VIDA '''
        if keys[pygame.K_e] and not self.damage_taken:
            self.vida -= 1 # para probar a bajar vida
            self.damage_taken = True
            self.damage_taken_time = pygame.time.get_ticks()

        # movimiento
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.orientacionAtaque = dinamic_sprites.UP
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.orientacionAtaque = dinamic_sprites.DOWN
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.orientacion = dinamic_sprites.RIGHT
            self.orientacionAtaque = dinamic_sprites.RIGHT
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.orientacion = dinamic_sprites.LEFT
            self.orientacionAtaque = dinamic_sprites.LEFT
        else:
            self.direction.x = 0

        self.postura = IDLE if self.direction.x == 0 and self.direction.y == 0 else ANDANDO

        # ataque
        if keys[pygame.K_SPACE] and not self.recargando:
            self.direction.x = 0
            self.direction.y = 0
            self.is_attacking = True
            self.tiempoAtaque = pygame.time.get_ticks()

            self.numImagenPostura = 0 # para que empiece a atacar desde la primera imagen
            self.postura = ATACANDO # postura atacando

            self.crear_ataque()


    def collision(self, direction):

        super().collision(direction)

        # if pygame.sprite.groupcollide(self.groups()[1], self.enemies_sprites, False, False) != {}:
        enemy_hitted = pygame.sprite.spritecollideany(self, self.enemies_sprites)
        if enemy_hitted and not self.damage_taken and not enemy_hitted.is_death:
            print("Lo has tocado - Perder vida")
            self.damage_taken = True
            self.damage_taken_time = pygame.time.get_ticks()
            self.hit_countdown = 6


    def cooldown(self):
        current_time = pygame.time.get_ticks()

        # cooldown para cuando se realiza un ataque
        if self.is_attacking:
            if current_time - self.tiempoAtaque > self.cooldownAtaque:
                self.is_attacking = False
                self.recargando = True
                self.tiempoRecarga = current_time

        elif self.recargando:
            if current_time - self.tiempoRecarga > self.cooldownRecarga:
                self.recargando = False
                self.borrar_ataque() 

        elif self.damage_taken:
            if current_time - self.damage_taken_time > self.cooldown_damage_taken:
                self.damage_taken = False


    def get_image(self):
        self.update_pose()
        if self.orientacion == dinamic_sprites.RIGHT:
            return self.image.subsurface(self.coordenadasHoja[self.postura][self.numImagenPostura])
        elif self.orientacion == dinamic_sprites.LEFT:
            return pygame.transform.flip(self.image.subsurface(self.coordenadasHoja[self.postura][self.numImagenPostura]), 1, 0)


    def get_orientacion(self):
        return self.orientacion


    def get_orientacionAtaque(self):
        return self.orientacionAtaque


    def update_pose(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = RETARDO_ANIMACION_JUGADOR[self.postura]
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.postura]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.postura])-1


    def update(self):
        self.input()
        self.cooldown()
        self.move(self.speed)