import configparser
import pygame
from director.scene import *
from pygame.locals import *

# -------------------------------------------------
# Lectura do ficheiro de configuración

parser = configparser.ConfigParser()
parser.read("GaiaStation.config")
SCREEN_WIDTH = int(parser.get("director", "SCREEN_WIDTH"))
SCREEN_HEIGHT = int(parser.get("director", "SCREEN_HEIGHT"))

class Director():

    def __init__(self):
        # Inicializamos a pantalla e o modo gráfico
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gaia Station")
        # Pila de escenas
        self.stack = []
        # Flag que indica cando queren salir da escena
        self.quit_scene = False
        self.clock = pygame.time.Clock()

    def loop(self, scene):
        self.quit_scene = False

        # Eliminamos todos os eventos producidos antes de entrar no bucle
        pygame.event.clear()
        
        # O bucle do xogo, as accións que se realicen faranse en cada escena
        while not self.quit_scene:
            tiempo_pasado = self.clock.tick(60)
            # Pasamos os eventos á escena
            scene.events(pygame.event.get())
            # Actualiza a escena
            scene.update(tiempo_pasado)
            # Debúxase na pantalla
            scene.draw(self.screen)
            pygame.display.flip()

    def execute(self):
        while (len(self.stack)>0):
            scene = self.stack[len(self.stack)-1]
            # Execútase o bucle de eventos ata que remate a escena
            self.loop(scene)

    def exit_scene(self):
        self.quit_scene = True
        # Eliminamos a escena actual da pila
        if (len(self.stack)>0):
            self.stack.pop()

    def quit_program(self):
        self.stack = []
        self.quit_scene = True

    def change_scene(self, scene):
        self.exit_scene()
        self.stack.append(scene)

    def stack_scene(self, scene):
        self.quit_scene = True
        self.stack.append(scene)
