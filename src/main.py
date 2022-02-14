#==============================================================================
#
#
#
#==============================================================================

import time
import numpy as np
import pygame
import sys

from pygame.locals import *

#==============================================================================
# Constantes

WHITE = (255, 255, 255)
GRAY = (75, 75, 75)

#==============================================================================
# Eventos

# ...

#==============================================================================
# Bucle principal

if __name__ == "__main__":

    # Inicializacion
    pygame.init()
    clock = pygame.time.Clock()

    pos_x = 50
    pos_y = 50

    # Configuracion inicial da pantalla
    screen = pygame.display.set_mode((800,600))
    screen.fill(GRAY)

    # Bucle de eventos
    while True:
        clock.tick(60)

        for evento in pygame.event.get():
                # RIGHT
                if evento.type == KEYDOWN and evento.key == K_RIGHT:
                    pos_x += 10
                
                # ESCAPE
                elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        screen.fill(GRAY)
        pygame.draw.circle(screen, WHITE, (pos_x, pos_y), 10, 0)
        pygame.display.update()

    



