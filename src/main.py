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
from level import Level

#==============================================================================
# Constantes

WHITE = (255, 255, 255)
GRAY = (75, 75, 75)
BLACK = (0, 0, 0)

#==============================================================================
# Eventos

# ...

#==============================================================================
# Bucle principal

if __name__ == "__main__":

    # Inicializacion
    pygame.init()
    clock = pygame.time.Clock()

    # Configuracion inicial da pantalla
    screen = pygame.display.set_mode((800,600))
    screen.fill(BLACK)
    
    # Permitimos que la tecla este pulsada
    # pygame.key.set_repeat(1, 25)

    # Eliminamos el raton
    pygame.mouse.set_visible(False)

    # Carga do nivel
    level = Level("level1.txt")

    # Bucle de eventos
    while True:
        clock.tick(60)

        for evento in pygame.event.get():
            # # RIGHT
            # if evento.type == KEYDOWN and evento.key == K_d:
            #     pos_x += 3

            # # LEFT
            # if evento.type == KEYDOWN and evento.key == K_a:
            #     pos_x -= 3

            # # UP
            # if evento.type == KEYDOWN and evento.key == K_w:
            #     pos_y -= 3

            # # DOWN  
            # if evento.type == KEYDOWN and evento.key == K_s:
            #     pos_y += 3
            
            # ESCAPE
            if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        level.run()
        
        # pygame.draw.circle(screen, WHITE, (pos_x, pos_y), 10, 0)
        pygame.display.update()

    



