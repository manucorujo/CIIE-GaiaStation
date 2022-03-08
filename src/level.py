from cv2 import sort
import pygame
from world_objects import *
from player import Player
from elementos_moviles import Proyectil
import configparser

#==============================================================================
# Clase para cargar un nivel

class Level:
    def __init__(self, filename):

        # Garda o ficheiro que define o nivel
        self.filename = filename

        # Obtén a superficie
        self.display_surface = pygame.display.get_surface()

        # Grupos de sprites
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprites para ataques
        self.ataque_actual = None

       # Lectura do ficheiro de configuración
        self.parser = configparser.ConfigParser()
        self.parser.read("GaiaStation.config")

        self.create_map()

    def create_map(self):

        # Usa o xestor de recursos para conseguir o mapa
        map = ResourcesManager.LoadLevelDefinitionFile(self.filename)
        TILE_SIZE = int(self.parser.get("level", "TILE_SIZE"))

        for y,line in enumerate(map.split("\n")):
            for x,simb in enumerate(line.split()):
                pos_x, pos_y = x*TILE_SIZE, y*TILE_SIZE
                if simb == 'p00':
                    print("posicionando xogador en: " + str(pos_x) + ',' + str(pos_y))
                    self.player = Player((pos_x,pos_y),[self.visible_sprites], self.obstacle_sprites, self.crear_ataque, self.borrar_ataque, "Player/Assault-Class.png", "Player/Assault-Class.txt")
                elif simb == 'w00':
                    Wall((pos_x,pos_y),[self.visible_sprites,self.obstacle_sprites], "Tileset/wall.png")

    def crear_ataque(self):
        self.ataque_actual = Proyectil(self.player, [self.visible_sprites], self.obstacle_sprites, "Projectiles/bullets+plasma.png", "Projectiles/bullets+plasma.txt", self.borrar_ataque)

    def borrar_ataque(self):
        if self.ataque_actual:
            self.ataque_actual.kill()
        self.ataque_actual = None

    def run(self):
        # mostrar os sprites dentro do grupo "visible_sprites"
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() # [x:0, y:0]
    
    def custom_draw(self,player):

        # Un poco de geometria y se entiende, jurado, el tema de movimiento de la camara.
        
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Tenemos que ordenar a los sprites por la posición en Y, por eso la Key es el rect.centery
        # Al ordenar por la posición en Y, se dibujará antes a un sprite que está por encima de otro,
        # por tanto, siguiendo el algoritmo del pintor que usar pygame por defecto el personaje se 
        # solapará correctamente estando por encima o por debajo de sprite. Si debajo tenemos una pared,
        # esta se dibujará después que nuestro personaje, y por tanto se superpondrá a él. (en base a su hitbox y el método collision)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.get_image(), offset_pos)