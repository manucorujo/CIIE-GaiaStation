import random
from resources_manager import *
from elementos_moviles import ElementoMovil
import pygame

# -------------------------------------------------

LEFT = 1
RIGHT = 2

IDLE = 0
WALKING = 1
FIRING = 2
MELEE = 3
DIYING = 4

HORIZONTAL = 1
VERTICAL = 2

ATTACK_DURATION = 300
ATTACK_COOLDOWN = 100

MOVE_DURATION = 500
MOVE_COOLDOWN = 500

NUM_FRAMES_PER_POSE = [2, 4, 2, 5, 1]
COOLDOWN_ANIMATION = [25, 0, 0, 0, 0]

# -------------------------------------------------

class MeleeEnemy(ElementoMovil):
    def __init__(self, pos, player, groups, obstacle_sprites, image_file, coordeanada_file):
        super().__init__(groups, obstacle_sprites, image_file)

        self.orientation = LEFT
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

        # A referencia do xogador
        self.player = player
        self.field_of_view = self.rect.inflate(160, 160)

        self.is_moving = False

        self.move_duration = MOVE_DURATION
        self.move_time = 0
        
        self.stop_duration = MOVE_DURATION
        self.stop_time = 0


    def move_ai(self):

        speed_buf = 1

        if self.is_hunting:
            speed_buf = 2
            self.direction.update(self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery)

        else:
            if pygame.Rect.colliderect(self.player.rect, self.field_of_view):
                self.is_hunting = True

        # Movemento
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed * speed_buf
        self.collision(HORIZONTAL)
        self.hitbox.y += self.direction.y * self.speed * speed_buf
        self.collision(VERTICAL)
        self.rect.center = self.hitbox.center


    def collision(self, direction):
        if direction == HORIZONTAL:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == VERTICAL:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: 
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: 
                        self.hitbox.top = sprite.hitbox.bottom


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
                self.stop_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.direction.y = 0

        elif not self.is_moving and not self.is_hunting:
            if current_time - self.stop_time > self.stop_duration:
                self.is_moving = True
                self.move_time = pygame.time.get_ticks()
                self.direction.x = random.randint(-1,1)
                self.direction.y = random.randint(-1,1)
            

    def get_image(self):
        self.update_pose()
        if self.orientation == RIGHT:
            return self.image.subsurface(self.coordinates_sheet[self.current_pose][self.current_pose_frame])
        elif self.orientation == LEFT:
            return pygame.transform.flip(self.image.subsurface(self.coordinates_sheet[self.current_pose][self.current_pose_frame]), 1, 0)


    def update_pose(self):
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
        self.move_ai()
