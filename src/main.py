#==============================================================================
#
# # TODO: Engadir sinatura en todos os ficheiros
#
#==============================================================================

import time
import numpy as np
import pygame
import sys

from pygame.locals import *
from level import Level

#==============================================================================
# Constantes

# TODO: Isto deberia sacarse a un script de configuracion mais adiante

WHITE = (255, 255, 255)
GRAY = (75, 75, 75)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#==============================================================================
# Clase PRincipal do xogo

class Game:
    
    def __init__ (self):
        # Inicializacion
        pygame.init()
        self.clock = pygame.time.Clock()

        # Configuracion inicial da pantalla
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("GAIA Station") # nome do xogo
        self.screen.fill(BLACK)

        # Permitimos que la tecla este pulsada
        # pygame.key.set_repeat(1, 25)

        # Eliminamos el raton
        pygame.mouse.set_visible(False)

        # Carga do nivel
        self.level = Level("level1.txt")

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

            self.screen.fill(BLACK)
            self.level.run()
            pygame.display.update()
        return

#==============================================================================
# Bucle principal

if __name__ == "__main__":
    game = Game()
    game.run()
    

    



