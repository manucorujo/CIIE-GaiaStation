import configparser
import random
import enemies
from resources_manager import *
import dinamic_sprites
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

ATTACK_DURATION = int(parser.get("melee_enemy", "ATTACK_DURATION"))
ATTACK_COOLDOWN = int(parser.get("melee_enemy", "ATTACK_COOLDOWN"))

MOVE_DURATION = int(parser.get("melee_enemy", "MOVE_DURATION"))
STOP_DURATION = int(parser.get("melee_enemy", "STOP_DURATION"))

NUM_FRAMES_PER_POSE = list(map(int, str.split(parser.get("melee_enemy", "NUM_FRAMES_PER_POSE"))))
COOLDOWN_ANIMATION = list(map(int, str.split(parser.get("melee_enemy", "COOLDOWN_ANIMATION"))))

# -------------------------------------------------

class MeleeEnemy(enemies.Enemy):
    def __init__(self, pos, player, groups, obstacle_sprites, image_file, coordeanada_file):
        super().__init__(player, groups, obstacle_sprites, image_file)

        self.orientation = dinamic_sprites.LEFT
        self.speed = 1
        self.current_pose = 0
        self.current_pose_frame = 0
        self.coordinates_sheet = []

        # Cargamos o arquivo de coordenadas
        datos = ResourcesManager.CargarArchivoCoordenadas(coordeanada_file)
        datos = datos.split()
        
        # Inicialización dos frames para as animacions
        cont = 0
        for pose in range(len(NUM_FRAMES_PER_POSE)):
            self.coordinates_sheet.append([])

            for frame in range(NUM_FRAMES_PER_POSE[pose]):
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
        
        # O rect do enemigo, da mesma forma ca do xogador, recortase por arriba
        # e por abaixo, para que poda achegarse ás paredes
        self.rect = pygame.Rect(
            pos[0],
            pos[1],
            self.coordinates_sheet[self.current_pose][self.current_pose_frame][2],
            self.coordinates_sheet[self.current_pose][self.current_pose_frame][3]
        )

        # A hitbox para detectar colisions
        self.hitbox = self.rect.inflate(0, -12)

        # Un cooldown do movemento para que non cambie de sprite moi rapido
        self.movement_cooldown = 0

        # Movemento
        self.direction = pygame.math.Vector2()  # Por defecto: [x:0, y:0]

        # Ataques
        self.is_hunting = False

        self.is_attacking = False
        self.attack_duration = ATTACK_DURATION
        self.attack_time = 0

        self.has_cooldown = False
        self.cooldown_duration = ATTACK_COOLDOWN
        self.cooldown_time = 0

        # O FOV para detectar ao xogador
        self.field_of_view = self.rect.inflate(160, 160)

        self.is_moving = False

        self.move_duration = MOVE_DURATION
        self.move_time = 0
        
        self.stop_duration = STOP_DURATION
        self.stop_time = 0


    def move_ai(self, speed):

        #TODO: Sacar los parametros de tamaño de pantalla constantes
        offset_x = (800/2)
        offset_y = (600/2)

        if self.is_hunting:
            self.direction.update(self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery)
            self.move(speed * 2.5)
        
        elif self.rect.x > self.player.rect.centerx - offset_x and self.rect.x < self.player.rect.centerx + offset_x \
            and self.rect.y > self.player.rect.centery - offset_y and self.rect.y < self.player.rect.centery + offset_y:

                self.move(speed)
                
                if pygame.Rect.colliderect(self.player.rect, self.field_of_view):
                    self.is_hunting = True


    def cooldown(self):
        current_time = pygame.time.get_ticks()

        # Cooldown para cando se realiza un ataque
        if self.is_attacking:
            if current_time - self.attack_time > self.attack_duration:
                self.is_attacking = False
                self.has_cooldown = True
                self.cooldown_time = current_time
        elif self.has_cooldown:
            if current_time - self.cooldown_time > self.cooldown_duration:
                self.has_cooldown = False
                self.borrar_ataque()

        # Cooldown para o movemento
        if self.is_moving and not self.is_hunting:
            if current_time - self.move_time > self.move_duration:
                self.is_moving = False
                self.current_pose = IDLE
                self.current_pose_frame = 0
                self.stop_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.direction.y = 0

        elif not self.is_moving and not self.is_hunting:
            if current_time - self.stop_time > self.stop_duration:
                self.is_moving = True
                self.current_pose = WALKING
                self.current_pose_frame = 0
                self.move_time = pygame.time.get_ticks()
                self.direction.x = random.randint(-1,1)
                self.direction.y = random.randint(-1,1)
            

    def get_image(self):
        self.update_pose()
        if self.orientation == dinamic_sprites.RIGHT:
            return self.image.subsurface(self.coordinates_sheet[self.current_pose][self.current_pose_frame])
        elif self.orientation == dinamic_sprites.LEFT:
            return pygame.transform.flip(self.image.subsurface(self.coordinates_sheet[self.current_pose][self.current_pose_frame]), 1, 0)


    def update_pose(self):

        if self.direction.x > 0:
            self.orientation = dinamic_sprites.RIGHT
        elif self.direction.x < 0:
            self.orientation = dinamic_sprites.LEFT

        self.movement_cooldown -= 1

        if (self.movement_cooldown < 0):

            self.movement_cooldown = COOLDOWN_ANIMATION[self.current_pose]
            self.current_pose_frame += 1

            if self.current_pose_frame >= len(self.coordinates_sheet[self.current_pose]):
                self.current_pose_frame = 0

            if self.current_pose_frame < 0:
                self.current_pose_frame = len(self.coordinates_sheet[self.current_pose])-1


    def update(self):
        self.cooldown()
        self.move_ai(self.speed)