import os, pygame
from pygame.locals import *

# Clase baleira con métodos de clase
class ResourcesManager(object):
    resources = {}
            
    @classmethod
    def LoadImage(cls, name, colorkey=None):

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
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, RLEACCEL)
            # Almacénase
            cls.resources[name] = image
            # Devólvese
            return image

    @classmethod
    def LoadLevelDefinitionFile(cls, name):
        # Se o nome do arquivo está nos recursos xa cargados
        if name in cls.resources:
            return cls.resources[name]
        # Se non está cargado previamente
        else:
            # Cárgase o recurso indicanso o nome da súa carpeta
            fullname = os.path.join('../res/levels', name)
            pfile=open(fullname,'r')
            data=pfile.read()
            pfile.close()
            # Almacénase
            cls.resources[name] = data
            # Devólvese
            return data
