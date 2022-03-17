from melee_enemy import MeleeEnemy
from world_objects import *
from player import Player
from ui import UIGroup, BarraVida, Puntuacion
import pygame
import configparser

#==============================================================================
# Clase para cargar un nivel

class Level:
    def __init__(self, map_image, obstacles_file):

        # Garda o ficheiro que define o nivel
        self.obstacles_file = obstacles_file

        # Obtén a superficie
        self.display_surface = pygame.display.get_surface()

        # Grupos de sprites
        self.ui_sprites = UIGroup()
        self.visible_sprites = CameraGroup(map_image)
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()

        # Lectura do ficheiro de configuración
        self.parser = configparser.ConfigParser()
        self.parser.read("GaiaStation.config")

        self.player = None
        
        self.tile_size = int(self.parser.get("level", "TILE_SIZE"))

        self.create_map()

        # Elementos UI
        barra_vida = BarraVida([self.ui_sprites], "UI/health-bars.png", "UI/health-bars.txt", self.player.vida)
        puntuacion = Puntuacion([self.ui_sprites], 0)

        self.player.add_observer(barra_vida)
        self.player.add_observer(puntuacion)

    def create_map(self):

        # Usa o xestor de recursos para conseguir o mapa
        obstacles = ResourcesManager.LoadLevelObstaclesFile(self.obstacles_file)

        for row_index, row in enumerate(obstacles):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x, y = col_index * self.tile_size, row_index * self.tile_size
                    if col == 'p':
                        self.player = Player((x,y), [self.visible_sprites, self.player_sprites], [self.obstacle_sprites, self.enemies_sprites], "Player/Assault-Class.png", "Player/Assault-Class.txt")
                    elif col == 'e':
                        MeleeEnemy((x,y), self.player, [self.visible_sprites, self.enemies_sprites], [self.obstacle_sprites], "Robots/Scarab.png", "Robots/Scarab.txt")
                    else:
                        Obstacle((x,y), [self.obstacle_sprites, self.visible_sprites], 'Obstacles/' + col + '.png', (255,0,245))

    def run(self):
        # mostrar os sprites dentro do grupo "visible_sprites"
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

        # mostrar os sprites dentro do grupo "ui_sprites"
        self.ui_sprites.custom_draw()
        self.ui_sprites.update()

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