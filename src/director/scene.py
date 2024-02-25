# SPDX-FileCopyrightText: 2024 Manu Corujo <manucorujo@gmail.com>
#
# SPDX-License-Identifier: MIT

import configparser


class Scene:

    def __init__(self, director):
        self.director = director

        # Para tener acceso a la hora de centrar textos
        self.parser = configparser.ConfigParser()
        self.parser.read("GaiaStation.config")
        self.width = int(self.parser.get("director", "SCREEN_WIDTH"))
        self.height = int(self.parser.get("director", "SCREEN_HEIGHT"))

    def update(self, *args):
        raise NotImplemented("Ten que implementar o método update.")

    def events(self, *args):
        raise NotImplemented("Ten que implementar o método eventos.")

    def draw(self, screen):
        raise NotImplemented("Ten que implementar o método debuxar.")