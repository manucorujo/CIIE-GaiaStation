import pygame

# Utils
import configparser
from math import *
from utils.constants import *
from utils.resources_manager import *
import controls.keyboardControl as ctrl

# Clases necesarias
from sprites.subject import Subject
from sprites.player.bullets import Projectile
from sprites.dynamic_sprites import DynamicSprites


# -------------------------------------------------
# Lectura do ficheiro de configuración

parser = configparser.ConfigParser()
parser.read("GaiaStation.config")

TILE_SIZE = int(parser.get("level", "TILE_SIZE"))

IDLE = int(parser.get("player", "IDLE"))
ANDANDO = int(parser.get("player", "ANDANDO"))
AGACHADO = int(parser.get("player", "AGACHADO"))
ATACANDO = int(parser.get("player", "ATACANDO"))
DIYING = int(parser.get("player", "DEAD"))

# esto de al animación y retardos del ataque está completamente abierto a cambios
TIEMPO_ATAQUE = int(parser.get("player", "TIEMPO_ATAQUE"))
TIEMPO_RECARGA = int(parser.get("player", "TIEMPO_RECARGA"))
RETARDO_ANIMACION_ATAQUE = int((60 * int(TIEMPO_ATAQUE / 2))/1000)

# la caurta posicion, ataque, hay que ajustarla y coordinarla
ANIMATION_TRANSITION_TIME = [50, 25, 0, RETARDO_ANIMACION_ATAQUE, 50, 50] # updates que durará cada imagen del personaje
# hay un valor para cada current_pose: el primero para idle, el segundo para andar, etc.

COOLDOWN_DAMAGE_TAKEN = int(parser.get("player", "COOLDOWN_DAMAGE_TAKEN"))
NUM_FRAMES_PER_POSE = [2, 2, 2, 2, 3, 5, 3]

# -------------------------------------------------

class Player(DynamicSprites, Subject):
    def __init__(self, pos, groups, collision_groups, image_file, coordeanada_file):
        DynamicSprites.__init__(self, groups, collision_groups, image_file, coordeanada_file, NUM_FRAMES_PER_POSE, ANIMATION_TRANSITION_TIME)
        Subject.__init__(self)

        self.current_pose = IDLE # current_pose idle
        self.current_pose_frame = 0

        # Hitbox: correspondese co rect da perxoase, pero recortado por arriba e por abaixo para asi ter un comportamento mais real cas paredes 
        self.rect = pygame.Rect(pos[0],pos[1],self.coordinates_sheet[self.current_pose][self.current_pose_frame][2],self.coordinates_sheet[self.current_pose][self.current_pose_frame][3])
        self.hitbox = self.rect.inflate(0, -round(TILE_SIZE * 1/3))

        # O retardo a hora de cambiar a imaxe do Sprite, para que non se faga moi rapido
        self.animation_delay = 0

        # orientation da peroxonase (der ou esq)
        self.orientation = RIGHT
        self.attack_orientation = RIGHT

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
        self.objects_sprites = collision_groups[2]
        self.goal_flag_sprites = collision_groups[3]

        # Estadisticas: vida, etc
        self.max_vida = 3 # golpes para morir
        self.vida = self.max_vida 
        self.speed = 3.5 # velocidad de movimiento
        self.puntos = 0
        self.goal = False
        self.lose = False

        self.control = ctrl.KeyboardControl()

    def input(self):

        if self.is_attacking or self.current_pose == DIYING:
            return

        keys = pygame.key.get_pressed() 

        # movimiento
        if self.control.up(keys):
            self.direction.y = -1
            self.attack_orientation = UP
        elif self.control.down(keys):
            self.direction.y = 1
            self.attack_orientation = DOWN
        else:
            self.direction.y = 0

        if self.control.right(keys):
            self.direction.x = 1
            self.attack_orientation = RIGHT
        elif self.control.left(keys):
            self.direction.x = -1
            self.attack_orientation = LEFT
        else:
            self.direction.x = 0

        self.current_pose = IDLE if self.direction.x == 0 and self.direction.y == 0 else ANDANDO

        # ataque
        if self.control.attack(keys) and not self.reloading:
            self.direction.x = 0
            self.direction.y = 0
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()

            self.current_pose_frame = 0 # para que empiece a atacar desde la primera imagen
            self.current_pose = ATACANDO # current_pose atacando

            self.crear_ataque()


    def collision(self, direction):

        super().collision(direction)

        enemy_hitted = pygame.sprite.spritecollideany(self, self.enemies_sprites)
        if enemy_hitted and not enemy_hitted.is_death:
            self.take_damage(1)

        object_touched = pygame.sprite.spritecollideany(self, self.objects_sprites)
        if object_touched:
            self.heal(object_touched.get_heal_value())
            object_touched.kill()

        if pygame.sprite.spritecollideany(self, self.goal_flag_sprites):
            self.goal = True
            self.notify_obervers()

            
    def heal(self, heal_value):
        if self.current_pose != DIYING:
            self.vida = min(self.vida + heal_value, self.max_vida)
            self.notify_obervers()

    def take_damage(self, damage=1):
        if not self.damage_taken and self.current_pose != DIYING:
            self.damage_taken = True
            self.damage_taken_time = pygame.time.get_ticks()
            self.hit_countdown = 6
            self.vida -= damage
            self.puntos -= 5 # perde 5 puntos por golpe
            if self.vida <= 0:
                self._die()
            self.notify_obervers()

    # separase nunha nova funcion por se queremos engadir novas formas de morir
    def _die(self):
        self.damage_taken = False
        self.direction.x = 0; self.direction.y = 0
        self.current_pose = DIYING
        self.current_pose_frame = 0

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

    def update_pose(self):

        if self.current_pose == DIYING and self.current_pose_frame == NUM_FRAMES_PER_POSE[DIYING] - 1:
            self.lose = True
            self.kill()
            self.notify_obervers()
            return 
        
        super().update_pose()

        # Parpadeo se recibimos dano
        if self.damage_taken:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def get_attackOrientation(self):
        return self.attack_orientation

    def update(self):
        self.input()
        self.cooldown()
        self.move(self.speed)

    def crear_ataque(self):
        self.ataque_actual = Projectile(self, self.visible_sprites, [self.obstacle_sprites, self.enemies_sprites], "Projectiles/bullets+plasma.png", "Projectiles/bullets+plasma.txt", self.borrar_ataque)

    def borrar_ataque(self):
        if self.ataque_actual:
            self.ataque_actual.kill()
        self.ataque_actual = None

    def sumar_puntos(self, puntos):
        self.puntos += puntos
        self.notify_obervers()

    def set_stats_dto(self, dto):
        if dto is not None:
            self.vida = dto.get_vida()
            self.puntos = dto.get_puntos()