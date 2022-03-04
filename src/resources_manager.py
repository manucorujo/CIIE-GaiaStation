import os, pygame
from pygame.locals import *

#==============================================================================
# Clase baleira con métodos de clase

class ResourcesManager(object):
    resources = {}
            
    @classmethod
    def LoadSprite(cls, path, colorkey=None):

        # Se o nome do arquivo está entre os recursos xa cargados
        if path in cls.resources:
            return cls.resources[path]
        # Se non se cargou anteriormente
        else:
            try:
                image = pygame.image.load(path)
            except pygame.error as message:
                print('Cannot load image: ' + path)
                raise SystemExit(message)
            image = image.convert()
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, RLEACCEL)
            # Almacénase
            cls.resources[path] = image
            # Devólvese
            return image

    @classmethod
    def LoadLevelDefinitionFile(cls, path):
        # Se o nome do arquivo está nos recursos xa cargados
        if path in cls.resources:
            return cls.resources[path]
        # Se non está cargado previamente
        else:
            # Cárgase o recurso indicanso o nome da súa carpeta
            pfile=open(path,'r')
            data=pfile.read()
            pfile.close()
            # Almacénase
            cls.resources[path] = data
            # Devólvese
            return data
