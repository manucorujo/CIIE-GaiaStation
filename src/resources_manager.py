import os, pygame
from csv import reader
from pygame.locals import *

#==============================================================================
# Clase baleira con métodos de clase

class ResourcesManager(object):
    resources = {}

    @classmethod
    def LoadSprite(cls, name, colorkey=None):

        # Se o nome do arquivo está entre os recursos xa cargados
        if name in cls.resources:
            return cls.resources[name]
        # Se non se cargou anteriormente
        else:
            fullname = os.path.join('../res/sprites', name)
            try:
                image = pygame.image.load(fullname)
            except pygame.error as message:
                print('Cannot load image: ' + fullname)
                raise SystemExit(message)
            image = image.convert()
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, RLEACCEL)

            # reescalado para ver como queda
            image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))

            # Almacénase
            cls.resources[name] = image
            # Devólvese
            return image

    @classmethod
    def LoadImage(cls, name):

        # Se o nome do arquivo está entre os recursos xa cargados
        if name in cls.resources:
            return cls.resources[name]
        # Se non se cargou anteriormente
        else:
            fullname = os.path.join('../res/images', name)
            try:
                image = pygame.image.load(fullname)
            except pygame.error as message:
                print('Cannot load image: ' + fullname)
                raise SystemExit(message)
            image = image.convert()

            # reescalado para ver como queda
            image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))

            # Almacénase
            cls.resources[name] = image
            # Devólvese
            return image

    @classmethod
    def loadFont(cls, name, size):
        # Si el name de archivo está entre los recursos ya cargados
        if (name, size) in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            fullname = os.path.join('../res/fonts', name)
            datos = pygame.font.Font(fullname, size)
            # Se almacena
            cls.resources[name] = datos
            # Se devuelve
            return datos

    @classmethod
    def LoadLevelObstaclesFile(cls, name):
        # Se o nome do arquivo está nos recursos xa cargados
        if name in cls.resources:
            return cls.resources[name]
        # Se non está cargado previamente
        else:
            # Cárgase o recurso indicanso o nome da súa carpeta
            fullname = os.path.join('../res/levels', name)
            data = []
            with open(fullname) as f:
                content = reader(f, delimiter = ',')
                for row in content:
                    data.append(list(row))
            # Almacénase
            cls.resources[name] = data
            # Devólvese
            return data

    @classmethod
    def CargarArchivoCoordenadas(cls, name):
        # Si el name de archivo está entre los recursos ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            fullname = os.path.join('../res/sprites', name)
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            # Se almacena
            cls.resources[name] = datos
            # Se devuelve
            return datos

    @classmethod
    def loadMusic(cls, name):
        # Si el name de archivo está entre los recursos ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            fullname = os.path.join('../res/music', name)
            datos = pygame.mixer.music.load(fullname)
            # Se almacena
            cls.resources[name] = datos
            # Se devuelve
            return datos
