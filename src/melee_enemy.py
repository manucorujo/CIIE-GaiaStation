import configparser
import random
import enemies
from objects import HeartObject
from resources_manager import *
import dynamic_sprites
import pygame

# -------------------------------------------------
# Lectura do ficheiro de configuración

parser = configparser.ConfigParser()
parser.read("GaiaStation.config")
IDLE = int(parser.get("melee_enemy", "IDLE"))
WALKING = int(parser.get("melee_enemy", "WALKING"))
FIRING = int(parser.get("melee_enemy", "FIRING"))
MELEE = int(parser.get("melee_enemy", "MELEE"))
DIYING = int(parser.get("melee_enemy", "DIYING"))

################## POR REVISAR ### COMENTARIO DE AG
ATTACK_DURATION = int(parser.get("melee_enemy", "ATTACK_DURATION"))
COOLDOWN_DURATION = int(parser.get("melee_enemy", "COOLDOWN_DURATION"))
################## POR REVISAR

MOVE_DURATION = int(parser.get("melee_enemy", "MOVE_DURATION"))
STOP_DURATION = int(parser.get("melee_enemy", "STOP_DURATION"))

NUM_FRAMES_PER_POSE = list(map(int, str.split(parser.get("melee_enemy", "NUM_FRAMES_PER_POSE"))))
COOLDOWN_ANIMATION = list(map(int, str.split(parser.get("melee_enemy", "COOLDOWN_ANIMATION"))))

# is_walking
WALK_DURATION = 1000

# damage_taken
INVENCIBILITY_DURATION = 200

# is_death
DEATH_DURATION = 200

NUM_FRAMES_PER_POSE = [2, 4, 2, 5, 1]
ANIMATION_TRANSITION_TIME = [25, 20, 0, 25, 100]

# -------------------------------------------------

class MeleeEnemy(enemies.Enemy):
    def __init__(self, pos, player, groups, collision_groups, image_file, coordeanada_file, speed, health):
        super().__init__(player, groups, collision_groups, image_file, coordeanada_file, NUM_FRAMES_PER_POSE, ANIMATION_TRANSITION_TIME, speed, health)

        self.orientation = dynamic_sprites.LEFT if random.randint(1,2) == 1 else dynamic_sprites.RIGHT
        self.current_pose = 0
        self.current_pose_frame = 0
        
        # O rect do enemigo, da mesma forma ca do xogador, recortase por arriba
        # e por abaixo, para que poda achegarse ás paredes
        self.rect = pygame.Rect(
            pos[0],
            pos[1],
            self.coordinates_sheet[self.current_pose][self.current_pose_frame][2],
            self.coordinates_sheet[self.current_pose][self.current_pose_frame][3]
        )

        # Parametros
        self.speed = speed
        self.health = health

        # A hitbox para detectar colisions
        self.hitbox = self.rect.inflate(0, -12)

        # Un cooldown do movemento para que non cambie de sprite moi rapido
        self.animation_delay = 0
        self.attack_count = 12

        # Movemento
        self.direction = pygame.math.Vector2()  # Por defecto: [x:0, y:0]

        # O FOV para detectar ao xogador
        self.field_of_view = None

        # O rango que ten o enemigo para atacar
        self.attack_range = None

        # Estados do enemigo
        self.player_detected = False
        self.is_walking = False
        self.is_attacking = False
        self.has_cooldown = False
        self.damage_taken = False
        self.is_death = False

        # Tempos para cada estado
        self.walk_time = pygame.time.get_ticks()
        self.attack_time = 0
        self.cooldown_time = 0
        self.damage_taken_time = 0
        self.death_time = 0


    def move_ai(self):
        #TODO: Sacar los parametros de tamaño de pantalla constantes
        offset_x = (800/2)
        offset_y = (600/2)

        is_visible = False
        speed_buff = 0

        self.field_of_view = self.rect.inflate(256, 256)
        self.attack_range = self.rect.inflate(6,6)

        if self.rect.x > self.player.rect.centerx - offset_x and self.rect.x < self.player.rect.centerx + offset_x \
            and self.rect.y > self.player.rect.centery - offset_y and self.rect.y < self.player.rect.centery + offset_y:
            # O enemigo está en pantalla
            is_visible = True

        if self.field_of_view.colliderect(self.player.rect) and not self.player_detected:
            # O xogador entrou no campo de visión do enemigo
            self.player_detected = True
            self._start_walking()

        if self.player_detected and self.is_walking:
            # Detectou ao xogador e está ao perseguir

            if self._is_player_in_attack_range() and not self.is_attacking and not self.has_cooldown:
                # O xogador está no rango de ataque do enemigo
                self._create_attack()
            else:
                # Todavía non alcanzou ao xogador
                self.direction.update(self.player.rect.centerx - self.rect.centerx,
                                      self.player.rect.centery - self.rect.centery)
                speed_buff = 2.5

        elif not self.player_detected and self.is_walking and is_visible:
            # Non detectou a ningún xogador e está paseando tranquilo
            speed_buff = 1

        self.move(self.speed * speed_buff)
        return


    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if self.player_detected:
            if self.is_attacking:
                self.attack_count -= 1
                if current_time - self.attack_time > ATTACK_DURATION:
                    self._delete_attack()

            elif self.has_cooldown:
                if current_time - self.cooldown_time > COOLDOWN_DURATION:
                    self._start_walking()

        else:
            if self.is_walking:
                if current_time - self.walk_time > WALK_DURATION:
                    self._stop_walking()
            else:
                if current_time - self.walk_time > WALK_DURATION:
                    dir_x = 0
                    dir_y = 0

                    while dir_x == 0 and dir_y == 0:
                        dir_x = random.uniform(-1.00, 1.00)
                        dir_y = random.uniform(-1.00, 1.00)

                    self.direction.update(dir_x, dir_y)
                    self._start_walking()

        if self.damage_taken:
            if current_time - self.damage_taken_time > INVENCIBILITY_DURATION:
                self.damage_taken = False
                self._start_walking()

        if self.is_death:
            if current_time - self.death_time > DEATH_DURATION:
                self.kill()
                self._generate_heart()
                self.player.sumar_puntos(10)
        return


    def _create_attack(self):
        self.is_attacking = True
        self.is_walking = False
        self.has_cooldown = False

        self.current_pose = MELEE
        self.current_pose_frame = 0

        self.attack_time = pygame.time.get_ticks()
        return


    def _delete_attack(self):
        if self._is_player_in_attack_range() and self.attack_count < 0:
            self.player.take_damage(1)

        self.is_attacking = False
        self.is_walking = False
        self.has_cooldown = True

        self.current_pose = IDLE
        self.current_pose_frame = 0

        self.cooldown_time = pygame.time.get_ticks()
        self.attack_count = 12
        return

    
    def _start_walking(self):
        self.is_attacking = False
        self.is_walking = True
        self.has_cooldown = False

        self.current_pose = WALKING
        self.current_pose_frame = 0

        self.walk_time = pygame.time.get_ticks()
        return

    
    def _stop_walking(self):
        self.is_attacking = False
        self.is_walking = False
        self.has_cooldown = False

        self.current_pose = IDLE
        self.current_pose_frame = 0

        self.walk_time = pygame.time.get_ticks()
        return

    
    def take_damage(self, damage):
        if not self.damage_taken:
            self._stop_walking()
            self.current_pose = FIRING
            self.current_pose_frame = 0
            self.health -= damage

            if self.health <= 0:
                self._die()
            
            self.player_detected = True
            self.damage_taken = True
            self.knockback_counter = 12
            self.damage_taken_time = pygame.time.get_ticks()
        return

    
    def _die(self):
        self.is_attacking = False
        self.player_detected = False
        self.is_walking = False
        self.has_cooldown = False
        self.damage_taken = False
        self.is_death = True

        self.current_pose = DIYING
        self.current_pose_frame = 0

        self.death_time = pygame.time.get_ticks()
        return

    
    #TODO: Revisar como generar corazones desde el nivel al morir un enemigo
    def _generate_heart(self):
        value = random.uniform(0,1)
        if value >= 0.8:
            print("Crear corazon")


    def _is_player_in_attack_range(self):
        return self.attack_range.colliderect(self.player.rect)


    def update(self):
        self.cooldown()
        self.move_ai()