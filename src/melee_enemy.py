import random
import enemies
from resources_manager import *
import dinamic_sprites
import pygame

# -------------------------------------------------

IDLE = 0
WALKING = 1
FIRING = 2
MELEE = 3
DIYING = 4

ENEMY_BASE_SPEED = 1
ENEMY_BASE_LIFE = 30

# is_attacking
ATTACK_DURATION = 300

# has_cooldown
COOLDOWN_DURATION = 700

# is_walking
WALK_DURATION = 1000

# damage_taken
INVENCIBILITY_DURATION = 200

# is_death
DEATH_DURATION = 200

NUM_FRAMES_PER_POSE = [2, 4, 2, 5, 1]
COOLDOWN_ANIMATION = [25, 20, 0, 25, 100]

# -------------------------------------------------

class MeleeEnemy(enemies.Enemy):
    def __init__(self, pos, player, groups, collision_groups, image_file, coordeanada_file):
        super().__init__(player, groups, collision_groups, image_file)

        self.orientation = dinamic_sprites.LEFT if random.randint(1,2) == 1 else dinamic_sprites.RIGHT
        self.orientacion = player.get_orientacionAtaque()
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

        # Parametros básicos do enemigo
        self.speed = ENEMY_BASE_SPEED
        self.health = ENEMY_BASE_LIFE

        # A hitbox para detectar colisions
        self.hitbox = self.rect.inflate(0, -12)

        # Un cooldown do movemento para que non cambie de sprite moi rapido
        self.movement_cooldown = 0
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
            self.player.perder_vida(1)

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

    
    def get_damage(self, damage):
        if not self.damage_taken:
            self._stop_walking()
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


    def _is_player_in_attack_range(self):
        return self.attack_range.colliderect(self.player.rect)


    def get_image(self):
        self.update_pose()
        if self.orientation == dinamic_sprites.RIGHT:
            return self.image.subsurface(self.coordinates_sheet[self.current_pose][self.current_pose_frame])
        elif self.orientation == dinamic_sprites.LEFT:
            return pygame.transform.flip(self.image.subsurface(self.coordinates_sheet[self.current_pose][self.current_pose_frame]), 1, 0)


    def update_pose(self):
        # TODO: unificar con player en clase padre
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

            elif self.current_pose_frame < 0:
                self.current_pose_frame = len(self.coordinates_sheet[self.current_pose])-1

        return


    def update(self):
        self.cooldown()
        self.move_ai()