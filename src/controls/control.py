# SPDX-FileCopyrightText: 2024 Manu Corujo <manucorujo@gmail.com>
#
# SPDX-License-Identifier: MIT

# -------------------------------------------------
# Clase Control
class Control():
    def __init__(self):
        self.up_key = None
        self.down_key = None
        self.left_key = None
        self.right_key = None
        self.attack_key = None

    # Estos métodos reciben los eventos y/o la lista de teclas/botones pulsados y 
    # dicen si se quiso realizar una acción determinada

    def up(self, keys):
        pass 

    def down(self, keys):
        pass

    def left(self, keys):
        pass

    def right(self, keys):
        pass

    def attack(self, keys):
        pass

    def pause(self, keys):
        pass

    def select(self, keys):
        pass

    # Metodos que asignan a una tecla/boton una accion concreta

    def set_up(self, key):
        self.up_key = key

    def set_down(self, key):
        self.down_key = key

    def set_left(self, key):
        self.left_key = key

    def set_right(self, key):
        self.right_key = key

    def set_attack(self, key):
        self.attack_key = key

    def set_pause(self, key):
        self.pause_key = key

    def set_select(self, key):
        self.select_key = key