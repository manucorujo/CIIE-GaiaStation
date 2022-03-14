#==============================================================================
#
# # TODO: Engadir sinatura en todos os ficheiros
#
#==============================================================================

import time
import numpy as np
import pygame
import sys
import configparser
import re

from pygame.locals import *
from level import Level

#==============================================================================
# Clase PRincipal do xogo

class Game:
    
    def __init__ (self):
        # Inicializacion
        pygame.init()
        self.clock = pygame.time.Clock()

        # Lectura do ficheiro de configuración
        self.parser = configparser.ConfigParser()
        self.parser.read("GaiaStation.config")

        # Configuracion inicial da pantalla
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("GAIA Station") # nome do xogo
        BLACK = self.getColour(self.parser.get("main", "BLACK"))
        self.screen.fill(BLACK)

        # Eliminamos el raton
        pygame.mouse.set_visible(False)

        # Carga do nivel
        # self.level = Level("level1.png", "level1_obstacles.csv")
        self.level = Level("level2.png", "level2_obstacles.csv")

        return

    def run (self):
        # Bucle de eventos
        while True:
            self.clock.tick(60)

            for evento in pygame.event.get():       
                # ESCAPE
                if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            BLACK = self.getColour(self.parser.get("main", "BLACK"))
            self.screen.fill(BLACK)
            self.level.run()
            pygame.display.update()
        return

    def getColour(self, text):
        pattern = r'\(([0-9]+), ([0-9]+), ([0-9]+)\)'
        match = re.match(pattern, text)
        colour = tuple((int(x) for x in match.groups()))     
        return colour    

#==============================================================================
# Bucle principal

if __name__ == "__main__":
    game = Game()
    game.run()
    

    



