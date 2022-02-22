import pygame 
from world_objects import *
from player import Player
from debug import debug

#==============================================================================
# Clase para cargar un nivel

class Level:
    def __init__(self, filename):

        # Garda o ficheiro que define o nivel
        self.filename = filename

        # Obtén a superficie
        self.display_surface = pygame.display.get_surface()

        # Grupos de sprites
        self.visible_sprites = YSortCameraGroup()
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
                    self.player = Player((pos_x,pos_y),[self.visible_sprites], self.obstacle_sprites)
                elif simb == 'w00':
                    Wall((pos_x,pos_y),[self.visible_sprites,self.obstacle_sprites])

    def run(self):
        # mostrar os sprites dentro do grupo "visible_sprites"
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        # debug(self.player.direction)

'''
YSort es porque vamos a ordenar los sprites por la coordenada y, de esa forma le daremos algo de overlap
'''
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() # [x:0, y:0]
    
    def custom_draw(self,player):

        '''
        Un poco de geometria y se entiende, jurado
        '''

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        