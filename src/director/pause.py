import sys
import pygame
from director.scene import Scene
from utils.resources_manager import ResourcesManager
from pygame.locals import *

class Pause(Scene):

    def __init__(self, director):
        Scene.__init__(self, director)

        self.image = ResourcesManager.LoadImage('pause.jpg')
        self.image = pygame.transform.scale(self.image, (800, 600))

    def update(self, *args):
        return

    def events(self, events_list):
        for event in events_list:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_p:
                    self.return_game()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect())

    def exit_program(self):
        pygame.quit()
        sys.exit()

    def return_game(self):
        self.director.exit_scene()

