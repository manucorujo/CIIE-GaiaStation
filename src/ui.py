from resources_manager import *
from mi_sprite import MiSprite
import pygame

class UIGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def custom_draw(self):
        for sprite in self.sprites():
            sprite.dibujar_ui()

class BarraVida(MiSprite):
    def __init__(self, groups, image_file, coordeanada_file, player):
        super().__init__(groups, image_file)

        self.display_surface = pygame.display.get_surface()
        
        self.player = player
        self.vida = self.player.vida

        # Leemos las coordenadas de un archivo de texto
        datos = ResourcesManager.CargarArchivoCoordenadas(coordeanada_file)
        datos = datos.split() 
        cont = 0
        numImagenes = [3]
        self.coordenadasHoja = []

        self.coordenadasHoja.append([])
        tmp = self.coordenadasHoja[0]
        for postura in range(1, numImagenes[0]+1):
            self.separacion_barras = int(datos[cont+2]) # se usa para colocarlas una a una
            tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (self.separacion_barras, int(datos[cont+3]))))
            cont += 4

    def update(self):
        self.vida = self.player.vida

    def dibujar_ui(self):
        # Si self.vida es distinto, no se dibuja nada
        if (self.vida == 1):
            self.display_surface.blit(self.image.subsurface(self.coordenadasHoja[0][2]), (10, 10))
        elif (self.vida == 2):
            self.display_surface.blit(self.image.subsurface(self.coordenadasHoja[0][1]), (10, 10))
            self.display_surface.blit(self.image.subsurface(self.coordenadasHoja[0][1]), (10 + self.separacion_barras, 10))
        elif (self.vida == 3):
            self.display_surface.blit(self.image.subsurface(self.coordenadasHoja[0][0]), (10, 10))
            self.display_surface.blit(self.image.subsurface(self.coordenadasHoja[0][0]), (10 + self.separacion_barras, 10))
            self.display_surface.blit(self.image.subsurface(self.coordenadasHoja[0][0]), (10 + self.separacion_barras * 2, 10))  