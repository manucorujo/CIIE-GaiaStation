import configparser
from resources_manager import *
import dinamic_sprites
import pygame

# -------------------------------------------------
# Lectura do ficheiro de configuración

parser = configparser.ConfigParser()
parser.read("GaiaStation.config")
RETARDO_ANIMACION_BALA = int(parser.get("bullets", "RETARDO_ANIMACION_BALA"))

# -------------------------------------------------

class Proyectil(dinamic_sprites.DinamicSprite):
    def __init__(self, player, groups, obstacle_sprites, image_file, coordeanada_file, borrar_ataque):
        super().__init__(groups, obstacle_sprites, image_file)
        self.orientacion = player.get_orientacionAtaque()

        # Leemos las coordenadas de un archivo de texto
        datos = ResourcesManager.CargarArchivoCoordenadas(coordeanada_file)
        datos = datos.split()
        self.numImagenPostura = 0
        cont = 0
        numImagenes = [3]
        self.coordenadasHoja = []
        for linea in range(0, 1):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4
        
        self.retardoAnimacion = RETARDO_ANIMACION_BALA
        self.speed = 3

        self.borrar_ataque = borrar_ataque
        
        # placement
        aux_img = self.get_image() # para que se cargue la imagen BIEN
        if self.orientacion == dinamic_sprites.RIGHT: 
            self.rect = aux_img.get_rect(midleft = player.rect.midright)
        elif self.orientacion == dinamic_sprites.LEFT:
            # se mide desde el 0,0, y el jugador ha sido girado... no se
            self.rect = aux_img.get_rect(midright = player.rect.midleft) # (player.rect.midleft[0] + player.rect.width, player.rect.midleft[1])) 
        elif self.orientacion == dinamic_sprites.UP:
            self.rect = aux_img.get_rect(midbottom = player.rect.midtop)
        elif self.orientacion == dinamic_sprites.DOWN:
            self.rect = aux_img.get_rect(midtop = player.rect.midbottom) # (player.rect.midbottom[0], player.rect.midbottom[1] + player.rect.height))


    def move(self, speed):
        if self.orientacion == dinamic_sprites.RIGHT:
            self.rect.x += speed
        elif self.orientacion == dinamic_sprites.LEFT:
            self.rect.x -= speed
        elif self.orientacion == dinamic_sprites.UP:
            self.rect.y -= speed
        elif self.orientacion == dinamic_sprites.DOWN:
            self.rect.y += speed
        self.collision('')

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.rect):
                self.borrar_ataque()


    def get_image(self):
        self.update_pose()
        if self.orientacion == dinamic_sprites.RIGHT:
            return self.image.subsurface(self.coordenadasHoja[0][self.numImagenPostura])
        elif self.orientacion == dinamic_sprites.LEFT:
            #return self.image.subsurface(self.coordenadasHoja[0][self.numImagenPostura])
            return pygame.transform.flip(self.image.subsurface(self.coordenadasHoja[0][self.numImagenPostura]), 0, 0)
        elif self.orientacion == dinamic_sprites.UP:
            return self.image.subsurface(self.coordenadasHoja[0][self.numImagenPostura])
        elif self.orientacion == dinamic_sprites.DOWN:
            return self.image.subsurface(self.coordenadasHoja[0][self.numImagenPostura])


    def update_pose(self):
        if self.numImagenPostura >= len(self.coordenadasHoja[0])-1:
            return
        self.retardoAnimacion -= 1
        # Miramos si ha pasado el retardo
        if (self.retardoAnimacion < 0):
            self.retardoAnimacion = RETARDO_ANIMACION_BALA
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
        
    def update(self):
        self.move(self.speed)
