# SPDX-FileCopyrightText: 2024 Manu Corujo <manucorujo@gmail.com>
#
# SPDX-License-Identifier: MIT

import pygame
import controls.control as control

# -------------------------------------------------
# Clase Control
class KeyboardControl(control.Control):
    def __init__(self):
        super().__init__()
        self.up_key = pygame.K_w
        self.down_key = pygame.K_s
        self.left_key = pygame.K_a
        self.right_key = pygame.K_d
        self.attack_key = pygame.K_SPACE
        self.pause_key = pygame.K_p
        self.select_key = pygame.K_RETURN

    # Estos métodos reciben los eventos y/o la lista de teclas/botones pulsados y 
    # dicen si se quiso realizar una acción determinada

    def up(self, keys):
        return keys[self.up_key]

    def down(self, keys):
        return keys[self.down_key]

    def left(self, keys):
        return keys[self.left_key]
    
    def right(self, keys):
        return keys[self.right_key]
    
    def attack(self, keys):
        return keys[self.attack_key]

    def pause(self, keys):
        return keys[self.pause_key]

    def select(self, keys):
        return keys[self.select_key]