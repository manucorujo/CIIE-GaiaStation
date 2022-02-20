import pygame 
from world_objects import *
from player import Player


class Level:
    def __init__(self, filename):

        # Garda o ficheiro que define o nivel
        self.filename = filename

        # Obtén a superficie
        self.display_surface = pygame.display.get_surface()

        # Grupos de sprites
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):

        # Usa o xestor de recursos para conseguir o mapa
        map = ResourcesManager.LoadLevelDefinitionFile(self.filename)

        for y,line in enumerate(map.split("\n")):
            for x,simb in enumerate(line.split()):
                pos_x, pos_y = x*16, y*16
                if simb == 'p00':
                    print("posicionando xogador en: " + str(pos_x) + ',' + str(pos_y))
                    Player((pos_x,pos_y),[self.visible_sprites])
                elif simb == 'w00':
                    Wall((pos_x,pos_y),[self.visible_sprites,self.obstacle_sprites])

    def run(self):
        # mostrar os sprites dentro do grupo "visible_sprites"
        self.visible_sprites.draw(self.display_surface)