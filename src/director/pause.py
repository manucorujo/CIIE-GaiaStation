import sys
import pygame

from utils.resources_manager import ResourcesManager
from director.scene import Scene
from pygame.locals import *

class Pause(Scene):

    def __init__(self, director):
        Scene.__init__(self, director)

        self.image = ResourcesManager.LoadImage('pause.jpg')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        font = ResourcesManager.loadFont("upheavtt.ttf", 52)
        self.title = font.render('PAUSA', True, (237, 82, 47))
        self.title_rect = self.title.get_rect()

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
        self.title_rect.center = (self.width // 2, self.height // 2 - 100)
        screen.blit(self.title, self.title_rect)

    def exit_program(self):
        pygame.quit()
        sys.exit()

    def return_game(self):
        self.director.exit_scene()
