from resources_manager import *
import mi_sprite
import pygame

RETARDO_ANIMACION_BALA = 7

# -------------------------------------------------
# Clase ElementoMovil
class ElementoMovil(mi_sprite.MiSprite):
    "Los Sprites que tendra este juego"
    def __init__(self, groups, obstacle_sprites, image_file):
        super().__init__(groups, image_file)
    
        self.obstacle_sprites = obstacle_sprites

    def move(self, speed):
        pass

    def actualizarPostura(self):
        pass

# -------------------------------------------------
# Clase Proyectil
class Proyectil(ElementoMovil):
    def __init__(self, player, groups, obstacle_sprites, image_file, coordeanada_file, borrar_ataque):
        super().__init__(groups, obstacle_sprites, image_file)
        self.orientacion = player.get_orientacion()

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
        if self.orientacion == 2: # derecha
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        else: # izquierda
            # se mide desde el 0,0, y el jugador ha sido girado... no se
            self.rect = self.image.get_rect(midright = (player.rect.midleft[0] + player.rect.width, player.rect.midleft[1])) 

    def move(self, speed):
        # pass
        self.rect.x += speed if self.orientacion == 2 else -speed
        self.collision('horizontal')

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.rect):
                self.borrar_ataque()


    def get_image(self):
        self.actualizarPostura()
        if self.orientacion == 2:
            return self.image.subsurface(self.coordenadasHoja[0][self.numImagenPostura])
        elif self.orientacion == 1:
            #return self.image.subsurface(self.coordenadasHoja[0][self.numImagenPostura])
            return pygame.transform.flip(self.image.subsurface(self.coordenadasHoja[0][self.numImagenPostura]), 0, 0)

    def actualizarPostura(self):
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
