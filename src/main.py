#==============================================================================
#
# # TODO: Engadir sinatura en todos os ficheiros
#
#==============================================================================

import pygame
import director
from director import *
from menu import Menu
from pygame.locals import *

#==============================================================================
# loop principal

if __name__ == "__main__":

    # Inicializamos a libraría de pygame
    pygame.init()
    # Creamos o director
    director = Director()
    # Creamos a escena coa pantalla inicial
    scene = Menu(director)
    # Decímoslle ao director que apile esta escena
    director.stack_scene(scene)
    director.execute()
    pygame.quit()
