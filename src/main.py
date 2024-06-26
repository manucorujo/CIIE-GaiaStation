# SPDX-FileCopyrightText: 2024 Manu Corujo <manucorujo@gmail.com>
#
# SPDX-License-Identifier: MIT

import director.director as director
from director.director import *
from director.menu import Menu
from pygame.locals import *
import pygame

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
