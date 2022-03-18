import configparser
import pygame
from resources_manager import *
import dynamic_sprites
from subject import Subject
from bullets import Projectile
from math import *

# -------------------------------------------------
# Lectura do ficheiro de configuración

parser = configparser.ConfigParser()
parser.read("GaiaStation.config")
IDLE = int(parser.get("player", "IDLE"))
ANDANDO = int(parser.get("player", "ANDANDO"))
AGACHADO = int(parser.get("player", "AGACHADO"))
ATACANDO = int(parser.get("player", "ATACANDO"))

# esto de al animación y retardos del ataque está completamente abierto a cambios
TIEMPO_ATAQUE = int(parser.get("player", "TIEMPO_ATAQUE"))
TIEMPO_RECARGA = int(parser.get("player", "TIEMPO_RECARGA"))
RETARDO_ANIMACION_ATAQUE = int((60 * int(TIEMPO_ATAQUE / 2))/1000)

# la caurta posicion, ataque, hay que ajustarla y coordinarla
RETARDO_ANIMACION_JUGADOR = [50, 25, 0, RETARDO_ANIMACION_ATAQUE] # updates que durará cada imagen del personaje
# hay un valor para cada postura: el primero para idle, el segundo para andar, etc.

COOLDOWN_DAMAGE_TAKEN = int(parser.get("player", "COOLDOWN_DAMAGE_TAKEN"))

# -------------------------------------------------

class Player(dynamic_sprites.DynamicSprite, Subject):
    def __init__(self, pos, groups, collision_groups, image_file, coordeanada_file):
        dynamic_sprites.DynamicSprite.__init__(self, groups, collision_groups, image_file)
        Subject.__init__(self)

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

        # Hitbox: correspondese co rect da perxoase, pero recortado por arriba e por abaixo para asi ter un comportamento mais real cas paredes 
        self.rect = pygame.Rect(pos[0],pos[1],self.coordenadasHoja[self.postura][self.numImagenPostura][2],self.coordenadasHoja[self.postura][self.numImagenPostura][3])
        self.hitbox = self.rect.inflate(0, -12)

        # O retardo a hora de cambiar a imaxe do Sprite, para que non se faga moi rapido
        self.retardoMovimiento = 0

        # Orientacion da peroxonase (der ou esq)
        self.orientacion = dynamic_sprites.RIGHT
        self.orientacion_ataque = dynamic_sprites.RIGHT

        # movemento
        self.direction = pygame.math.Vector2() # [x:0, y:0]

        # cooldowns
        self.is_attacking = False
        self.cooldown_ataque = TIEMPO_ATAQUE
        self.attack_time = 0

        self.reloading = False
        self.cooldown_reloading = TIEMPO_RECARGA
        self.reloading_time = 0

        self.damage_taken = False
        self.cooldown_damage_taken = COOLDOWN_DAMAGE_TAKEN
        self.damage_taken_time = 0

        # armas
        self.ataque_actual = None
        self.visible_sprites = [groups[0]]

        # Grupos para colisions
        self.obstacle_sprites = collision_groups[0]
        self.enemies_sprites = collision_groups[1]

        # Estadisticas: vida, etc
        self.max_vida = 3 # golpes para morir
        self.vida = self.max_vida 
        self.speed = 3.5 # velocidad de movimiento

        self.puntos = 0


    def input(self):

        if self.is_attacking:
            return

        keys = pygame.key.get_pressed()

        # movimiento
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.orientacion_ataque = dynamic_sprites.UP
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.orientacion_ataque = dynamic_sprites.DOWN
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.orientacion = dynamic_sprites.RIGHT
            self.orientacion_ataque = dynamic_sprites.RIGHT
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.orientacion = dynamic_sprites.LEFT
            self.orientacion_ataque = dynamic_sprites.LEFT
        else:
            self.direction.x = 0

        self.postura = IDLE if self.direction.x == 0 and self.direction.y == 0 else ANDANDO

        # ataque
        if keys[pygame.K_SPACE] and not self.reloading:
            self.direction.x = 0
            self.direction.y = 0
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()

            self.numImagenPostura = 0 # para que empiece a atacar desde la primera imagen
            self.postura = ATACANDO # postura atacando

            self.crear_ataque()


    def collision(self, direction):

        super().collision(direction)

        # TODO: seria mellor cambiar o nome da varaible?
        enemy_hitted = pygame.sprite.spritecollideany(self, self.enemies_sprites)
        if enemy_hitted and not enemy_hitted.is_death:
            self.perder_vida(1)
            

    def perder_vida(self, damage=1):
        if not self.damage_taken:
            self.damage_taken = True
            self.damage_taken_time = pygame.time.get_ticks()
            self.hit_countdown = 6
            self.vida -= damage
            self.notify_obervers()


    def cooldown(self):
        current_time = pygame.time.get_ticks()

        # cooldown para cuando se realiza un ataque
        if self.is_attacking:
            if current_time - self.attack_time > self.cooldown_ataque:
                self.is_attacking = False
                self.reloading = True
                self.reloading_time = current_time

        elif self.reloading:
            if current_time - self.reloading_time > self.cooldown_reloading:
                self.reloading = False
                self.borrar_ataque() 

        elif self.damage_taken:
            if current_time - self.damage_taken_time > self.cooldown_damage_taken:
                self.damage_taken = False


    def get_image(self):
        self.update_pose()
        if self.orientacion == dynamic_sprites.RIGHT:
            return self.image.subsurface(self.coordenadasHoja[self.postura][self.numImagenPostura])
        elif self.orientacion == dynamic_sprites.LEFT:
            return pygame.transform.flip(self.image.subsurface(self.coordenadasHoja[self.postura][self.numImagenPostura]), 1, 0)


    def get_orientacionAtaque(self):
        return self.orientacion_ataque


    def update_pose(self):
        # TODO: unificar con melee_enemy en la clase padre
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
        
        # Parpadeo se recibimos dano
        if self.damage_taken:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.input()
        self.cooldown()
        self.move(self.speed)

    # Obtenemos la frecuncia del parpadeo (subir a la clase padre de enemigos y player)
    # def wave_value(self):
    #     value = sin(pygame.time.get_ticks())
    #     return 255 if value >= 0 else 0

    def crear_ataque(self):
        self.ataque_actual = Projectile(self, self.visible_sprites, [self.obstacle_sprites, self.enemies_sprites], "Projectiles/bullets+plasma.png", "Projectiles/bullets+plasma.txt", self.borrar_ataque)

    def borrar_ataque(self):
        if self.ataque_actual:
            self.ataque_actual.kill()
        self.ataque_actual = None

    def sumar_puntos(self, puntos):
        self.puntos += puntos
        self.notify_obervers()