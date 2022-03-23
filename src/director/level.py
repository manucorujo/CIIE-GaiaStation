from director.pause import Pause
from sprites.miscelaneous.objects import HeartObject
from sprites.observer import Observer, SpriteObserver
from director.scene import Scene
from sprites.npcs.melee_enemy import MeleeEnemy
from sprites.miscelaneous.world_objects import Obstacle, Flag
from sprites.player.player_dto import PlayerDTO
from utils.resources_manager import *
from sprites.player.player import Player
from sprites.miscelaneous.ui import UIGroup, BarraVida, Puntuacion
import pygame
import random
import configparser

#==============================================================================

enemies_types_list = [
    ({
        # Scarab
        "name" : "Robots/Scarab",
        "speed" : 1.1,
        "health" : 2
    }, 35),
    ({
        # Spider
        "name" : "Robots/Spider",
        "speed" : 1,
        "health" : 3
    }, 65)
]

#==============================================================================
# Clase para cargar un nivel

class Level(Scene, Observer):
    def __init__(self, director, map_image, obstacles_file, dto):
        Scene.__init__(self, director)

        # Garda o ficheiro que define o nivel
        self.obstacles_file = obstacles_file

        # Obtén a superficie
        self.display_surface = pygame.display.get_surface()

        # Grupos de sprites
        self.ui_sprites = UIGroup()
        self.visible_sprites = CameraGroup(map_image)
        self.obstacle_sprites = pygame.sprite.Group()
        self.objects_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.goal_flag_sprites = pygame.sprite.Group()

        # Observadores para os enemigos/obxectos
        self.hearts_observer = None
        self.enemies_counter_observer = None

        self.weighted_enemies_types = self._get_enemies_thresholds(enemies_types_list)

        # Lectura do ficheiro de configuración
        self.parser = configparser.ConfigParser()
        self.parser.read("GaiaStation.config")

        self.player = None
        self.alive_enemies = 0
        self.goal = False ### TODO: En un futuro se puede quitar
        self.lose = False
        
        self.tile_size = int(self.parser.get("level", "TILE_SIZE"))

        self.init_observers()
        self.create_map()

        # engadir dto
        self.player.set_stats_dto(dto)

        # Elementos UI
        barra_vida = BarraVida([self.ui_sprites], "UI/health-bars.png", "UI/health-bars.txt", self.player.vida)
        puntuacion = Puntuacion([self.ui_sprites], self.player.puntos)

        self.player.add_observer(barra_vida)
        self.player.add_observer(puntuacion)
        self.player.add_observer(self) # o level tamen observa, para ver se terminou

        ResourcesManager.loadMusic('level.mp3')
        pygame.mixer.music.play(loops=-1)

    def init_observers(self):
        self.hearts_observer = Level.HeartsGenerator(self)
        self.enemies_counter_observer = Level.EnemiesCounter(self)

    def create_map(self):

        # Usa o xestor de recursos para conseguir o mapa
        obstacles = ResourcesManager.LoadLevelObstaclesFile(self.obstacles_file)

        for row_index, row in enumerate(obstacles):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x, y = col_index * self.tile_size, row_index * self.tile_size
                    if col == '0':
                        self.player = Player((x,y), [self.visible_sprites, self.player_sprites], [self.obstacle_sprites, self.enemies_sprites, self.objects_sprites, self.goal_flag_sprites], "Player/Assault-Class.png", "Player/Assault-Class.txt")
                    elif col == '1':
                        self.alive_enemies += 1
                        self._generate_random_enemy((x,y))
                    elif col == 'f':
                        Flag((x,y), (self.tile_size, self.tile_size), [self.goal_flag_sprites])
                    else:
                        Obstacle((x,y), [self.obstacle_sprites, self.visible_sprites], 'Obstacles/' + col + '.png', (255,0,245))

    def _get_enemies_thresholds(self, enemies_types_list):
        weighted_enemies_types = []
        for (e_type, percent) in enemies_types_list:
            [weighted_enemies_types.append(e_type) for _ in range(0, percent)]
        return weighted_enemies_types

    def _generate_random_enemy(self, pos):
        enemy_type = random.choice(self.weighted_enemies_types)
        image = enemy_type["name"] + ".png"
        coord_file = enemy_type["name"] + ".txt"
        speed = enemy_type["speed"]
        health = enemy_type["health"]

        observers = {
            "hearts": self.hearts_observer, 
            "counter": self.enemies_counter_observer
        }

        MeleeEnemy( pos, self.player, [self.visible_sprites, self.enemies_sprites], [self.obstacle_sprites], 
                        image, coord_file, speed, health, observers)
        return

    def events(self, events_list):
        for event in events_list:
            if event.type == KEYDOWN:
                # Si la tecla es Escape
                if event.key == K_ESCAPE:
                    # Se sale del programa
                    self.director.quit_program()
                if event.key == K_p:
                    pause = Pause(self.director)
                    self.director.stack_scene(pause)

                # if e then goal = True
                if event.key == K_e:
                    self.goal = True
                    self.player.notify_obervers()

            if event.type == pygame.QUIT:
                self.director.quit_program()

    def draw(self, screen):
        self.visible_sprites.custom_draw(self.player)
        self.ui_sprites.custom_draw()

    def update(self, time):
        self.visible_sprites.update()
        self.ui_sprites.update()

    #==========================================================================

    class HeartsGenerator(SpriteObserver):

        def __init__(self, level):
            self.level = level

        def notify(self, enemy_pos):
            threshold = 1 - (self.level.player.vida * 0.3)
            value = random.uniform(0, 1)
            if value <= threshold:
                groups = [self.level.visible_sprites, self.level.objects_sprites]
                HeartObject(enemy_pos, groups, "Objects/heart.png")
            return

    #==========================================================================

    class EnemiesCounter(SpriteObserver):

        def __init__(self, level):
            self.level = level

        def notify(self, enemy_pos):
            if (self.level.obstacles_file == 'level1_obstacles.csv' or
                self.level.obstacles_file == 'level2_obstacles.csv'):
                self.level.alive_enemies -= 1
                if (self.level.alive_enemies == 0): 
                    self.level.goal = True
            return

#==============================================================================

class Level1(Level):
    def __init__(self, director, map_image, obstacles_file, dto):
        super().__init__(director, map_image, obstacles_file, dto)

    def notify(self,player):
        self.lose = player.lose
        dto = PlayerDTO(player)
        if self.lose:
            dead = Final(self.director, False)
            self.director.stack_scene(Level1(self.director, 'level1.png', 'level1_obstacles.csv', dto))
            self.director.stack_scene(dead)
        elif self.goal:
            level = Level2(self.director, 'level2.png', 'level2_obstacles.csv', dto)
            self.director.stack_scene(level)

#==============================================================================

class Level2(Level):
    def __init__(self, director, map_image, obstacles_file, dto):
        super().__init__(director, map_image, obstacles_file, dto)

    def notify(self,player):
        self.lose = player.lose
        dto = PlayerDTO(player)
        if self.lose:
            dead = Final(self.director, False)
            self.director.stack_scene(Level2(self.director, 'level2.png', 'level2_obstacles.csv', dto))
            self.director.stack_scene(dead)
        elif self.goal:
            level = Level3(self.director, 'level3.png', 'level3_obstacles.csv', dto)
            self.director.stack_scene(level)

#==============================================================================

class Level3(Level):
    def __init__(self, director, map_image, obstacles_file, dto):
        super().__init__(director, map_image, obstacles_file, dto)

    def notify(self,player):
        self.goal = player.goal
        self.lose = player.lose
        dto = PlayerDTO(player)
        if self.lose:
            dead = Final(self.director, False)
            self.director.stack_scene(Level3(self.director, 'level3.png', 'level3_obstacles.csv', dto))
            self.director.stack_scene(dead)
        elif self.goal:
            victory = Final(self.director, True)
            self.director.stack_scene(victory)

#==============================================================================

class CameraGroup(pygame.sprite.Group):
    def __init__(self, map_image):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() # [x:0, y:0]

        # Creando o chan
        self.floor_surf = ResourcesManager.LoadImage('maps/' + map_image)
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
    
    def custom_draw(self,player):

        # Un poco de geometria y se entiende, jurado, el tema de movimiento de la camara.
        
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # evitamos que la camara se mueva fuera del mapa
        if self.offset.x < self.floor_rect.left:
            self.offset.x = self.floor_rect.left
        elif self.offset.x > self.floor_rect.right - self.half_width*2:
            self.offset.x = self.floor_rect.right - self.half_width*2
        
        if self.offset.y < self.floor_rect.top:
            self.offset.y = self.floor_rect.top
        elif self.offset.y > self.floor_rect.bottom - self.half_height*2:
            self.offset.y = self.floor_rect.bottom - self.half_height*2


        # Debuxando o chan
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Tenemos que ordenar a los sprites por la posición en Y, por eso la Key es el rect.centery
        # Al ordenar por la posición en Y, se dibujará antes a un sprite que está por encima de otro,
        # por tanto, siguiendo el algoritmo del pintor que usar pygame por defecto el personaje se 
        # solapará correctamente estando por encima o por debajo de sprite. Si debajo tenemos una pared,
        # esta se dibujará después que nuestro personaje, y por tanto se superpondrá a él. (en base a su hitbox y el método collision)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.get_image(), offset_pos)

#==============================================================================

class Final(Scene):

    def __init__(self, director, win):
        Scene.__init__(self, director)

        self.image = ResourcesManager.LoadImage('black.jpg')
        self.image = pygame.transform.scale(self.image, (800, 600))
        title_font = ResourcesManager.loadFont("upheavtt.ttf", 52)
        text_font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        self.title = title_font.render('VICTORIA', True, (0, 255, 0)) if win else title_font.render('DERROTA', True, (255, 0, 0))
        self.text = text_font.render('Pulsa R para reiniciar', True, (255, 255, 255))

    def update(self, *args):
        return

    def events(self, events_list):
        for event in events_list:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exit_program()
                elif event.key == K_r:
                    self.director.exit_scene()
            elif event.type == pygame.QUIT:
                self.exit_program()

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect())
        screen.blit(self.title, (300, 210))
        screen.blit(self.text, (235, 300))
