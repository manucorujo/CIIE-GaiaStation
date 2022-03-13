import pygame
from resources_manager import *
import elementos_moviles

IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4

IDLE = 0
ANDANDO = 1
AGACHADO = 2 # sin usar
ATACANDO = 3

HORIZONTAL = 1
VERTICAL = 2

# esto de al animación y retardos del ataque está completamente abierto a cambios
TIEMPO_ATAQUE = 300
TIEMPO_RECARGA = 600
RETARDO_ANIMACION_ATAQUE = int((60 * int(TIEMPO_ATAQUE / 2))/1000)

# la caurta posicion, ataque, hay que ajustarla y coordinarla
RETARDO_ANIMACION_JUGADOR = [50, 25, 0, RETARDO_ANIMACION_ATAQUE] # updates que durará cada imagen del personaje
# hay un valor para cada postura: el primero para idle, el segundo para andar, etc.

COOLDOWN_DAMAGE_TAKEN = 1500

#==============================================================================
# Clase Player

class Player(elementos_moviles.ElementoMovil):
    def __init__(self, pos, groups, obstacle_sprites, enemies_sprites, crear_ataque, borrar_ataque, image_file, coordeanada_file):
        super().__init__(groups, obstacle_sprites, image_file)

        # Leemos las coordenadas de un archivo de texto
        datos = ResourcesManager.CargarArchivoCoordenadas(coordeanada_file)
        datos = datos.split()
        self.postura = IDLE # postura idle
        self.numImagenPostura = 0
        cont = 0
        numImagenes = [2, 2, 2, 2, 3, 5, 3]
        self.coordenadasHoja = []
        for linea in range(0, 7):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # Hitbox: se corresponde al rect del personaje, pero recortando por arriba y por abajo para así tener un comportamiento más realista con las paredes superiores e inferiores
        self.rect = pygame.Rect(pos[0],pos[1],self.coordenadasHoja[self.postura][self.numImagenPostura][2],self.coordenadasHoja[self.postura][self.numImagenPostura][3])
        self.hitbox = self.rect.inflate(0, -12)

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0

        # Orientacion del personaja (der o izq)
        self.orientacion = DERECHA
        self.orientacionAtaque = DERECHA

        # movimiento
        self.direction = pygame.math.Vector2() # [x:0, y:0]

        # cooldowns
        self.atacando = False
        self.cooldownAtaque = TIEMPO_ATAQUE
        self.tiempoAtaque = 0

        self.recargando = False
        self.cooldownRecarga = TIEMPO_RECARGA
        self.tiempoRecarga = 0

        self.damage_taken = False
        self.cooldown_damage_taken = COOLDOWN_DAMAGE_TAKEN
        self.damage_taken_time = 0

        # armas
        self.crear_ataque = crear_ataque
        self.borrar_ataque = borrar_ataque

        # Grupos
        self.obstacle_sprites = obstacle_sprites
        self.enemies_sprites = enemies_sprites

        # Estadisticas: vida, etc
        self.max_vida = 3 # golpes para morir
        self.vida = self.max_vida 
        self.speed = 3 # velocidad de movimiento

        # Por ordenar
        self.value = 0
        self.backup_image = self.image.copy()
        self.newColor = [0,0,0,0]


    def input(self):

        if self.atacando:
            return

        keys = pygame.key.get_pressed()

        ''' TEST PARA PERDER VIDA '''
        if keys[pygame.K_e] and not self.damage_taken:
            self.vida -= 1 # para probar a bajar vida
            self.damage_taken = True
            self.damage_taken_time = pygame.time.get_ticks()

        # movimiento
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.orientacionAtaque = ARRIBA
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.orientacionAtaque = ABAJO
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.orientacion = DERECHA
            self.orientacionAtaque = DERECHA
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.orientacion = IZQUIERDA
            self.orientacionAtaque = IZQUIERDA
        else:
            self.direction.x = 0

        self.postura = IDLE if self.direction.x == 0 and self.direction.y == 0 else ANDANDO

        # ataque
        if keys[pygame.K_SPACE] and not self.recargando:
            self.direction.x = 0
            self.direction.y = 0
            self.atacando = True
            self.tiempoAtaque = pygame.time.get_ticks()

            self.numImagenPostura = 0 # para que empiece a atacar desde la primera imagen
            self.postura = ATACANDO # postura atacando

            self.crear_ataque()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() # devuelve un vector con la misma direccion pero con magnitud 1
        
        # Uso de round -> el rect (hitbox) funciona con numero enteros, si no usamos round, el rect automaticamente 
        # redondeara a la baja, dando un comportamiento distinto entre valores negativos y positivos

        self.hitbox.x += round(self.direction.x * speed)
        self.collision(HORIZONTAL)
        self.hitbox.y += round(self.direction.y * speed)
        self.collision(VERTICAL)
        self.rect.center = self.hitbox.center # importante mantener el centro del rect

    def collision(self, direction):
        if direction == HORIZONTAL:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # nos movemos a la derecha
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == VERTICAL:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # hacia abajo
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: 
                        self.hitbox.top = sprite.hitbox.bottom

        if pygame.sprite.groupcollide(self.groups()[1], self.enemies_sprites, False, False) != {}:
            if not self.damage_taken:
                print("Golpe recibido")
                self.damage_taken = True
                self.damage_taken_time = pygame.time.get_ticks()
                self.hit_countdown = 6

    def cooldown(self):
        current_time = pygame.time.get_ticks()

        # cooldown para cuando se realiza un ataque
        if self.atacando:
            if current_time - self.tiempoAtaque > self.cooldownAtaque:
                self.atacando = False
                self.recargando = True
                self.tiempoRecarga = current_time

        elif self.recargando:
            if current_time - self.tiempoRecarga > self.cooldownRecarga:
                self.recargando = False
                self.borrar_ataque() 

        elif self.damage_taken:
            if current_time - self.damage_taken_time > self.cooldown_damage_taken:
                self.damage_taken = False

        # se añadiran más, como por ejemplo uno pequeño de invencibilidad para cuando se recibe un golpe

    def get_image(self):
        self.actualizarPostura()
        if self.orientacion == DERECHA:
            return self.image.subsurface(self.coordenadasHoja[self.postura][self.numImagenPostura])
        elif self.orientacion == IZQUIERDA:
            return pygame.transform.flip(self.image.subsurface(self.coordenadasHoja[self.postura][self.numImagenPostura]), 1, 0)

    def get_orientacion(self):
        return self.orientacion

    def get_orientacionAtaque(self):
        return self.orientacionAtaque

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = RETARDO_ANIMACION_JUGADOR[self.postura]
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.postura]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.postura])-1

    def update(self):
        self.input()
        self.cooldown()
        self.move(self.speed)