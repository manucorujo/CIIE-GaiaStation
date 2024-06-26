# SPDX-FileCopyrightText: 2024 Manu Corujo <manucorujo@gmail.com>
#
# SPDX-License-Identifier: MIT

import configparser
import sys
import pygame
from pygame.locals import *
from director.scene import Scene
from director.level import Level1
from utils.resources_manager import *
from itertools import cycle

# -------------------------------------------------
# Clase abstracta GUIElement

class GUIElement:
    def __init__(self, screen, rectangle):
        self.screen = screen
        self.rect = rectangle

    def set_up_position(self, position):
        (positionx, positiony) = position
        self.rect.left = positionx
        self.rect.bottom = positiony

    def position_in_element(self, position):
        (positionx, positiony) = position
        if (positionx>=self.rect.left) and (positionx<=self.rect.right) and (positiony>=self.rect.top) and (positiony<=self.rect.bottom):
            return True
        else:
            return False

# -------------------------------------------------
# Clase GUIText e os distintos textos

class GUIText(GUIElement):
    def __init__(self, screen, font, color, text, position):
        # Créase a imaxe do texto
        self.image = font.render(text, True, color)
        # Chámase ao método da clase ancestro co rectángulo que ocupa a imaxe
        GUIElement.__init__(self, screen, self.image.get_rect())
        # Colócase o rectángulo na súa posición
        self.set_up_position(position)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class PlayText(GUIText):
    def __init__(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Xogar', (380, 300))

    def select(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (138, 41, 10), 'Xogar', (380, 300))

    # Igual que o __init__, pero replícoo porque só son dúas líneas e ao chamar á función
    # enténdese mellor así o funcionamento
    def unselect(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Xogar', (380, 300))

    def action(self):
        self.screen.menu.execute_game()

class ConfigText(GUIText):
    def __init__(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Configuración', (330, 335))
    
    def select(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (138, 41, 10), 'Configuración', (330, 335))

    def unselect(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Configuración', (330, 335))

    def action(self):
        self.screen.menu.show_config_screen()

class ExitText(GUIText):
    def __init__(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Saír', (382, 370))

    def select(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (138, 41, 10), 'Saír', (382, 370))

    def unselect(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Saír', (382, 370))

    def action(self):
        self.screen.menu.exit_program()

class ReturnText(GUIText):
    def __init__(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Volver', (50, 200))

    def select(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (138, 41, 10), 'Volver', (50, 200))

    def unselect(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Volver', (50, 200))

    def action(self):
        self.screen.menu.return_screen()

class SetVolumeText(GUIText):
    def __init__(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Volume: ' + str(round(pygame.mixer.music.get_volume() * 10)), (50, 250))

    def select(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (138, 41, 10), 'Volume: ' + str(round(pygame.mixer.music.get_volume() * 10)), (50, 250))

    def unselect(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Volume: ' + str(round(pygame.mixer.music.get_volume() * 10)), (50, 250))

    def action(self):
        return

    def minus(self):
        pygame.mixer.music.set_volume(round(pygame.mixer.music.get_volume() - 0.1, 1))

    def plus(self):
        pygame.mixer.music.set_volume(round(pygame.mixer.music.get_volume() + 0.1, 1))

class ToggleFullScreem(GUIText):
    def __init__(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Cambiar entre pantalla completa ou ventá', (50, 300))

    def select(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (138, 41, 10), 'Cambiar entre pantalla completa ou ventá', (50, 300))

    def unselect(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Cambiar entre pantalla completa ou ventá', (50, 300))

    def action(self):
        pygame.display.toggle_fullscreen()

class TitleText(GUIText):
    def __init__(self, screen):
        font = ResourcesManager.load_font("upheavtt.ttf", 52)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'GAIA STATION', (260, 250))

# -------------------------------------------------
# Clase GUIScreen e as distintas pantallas

class GUIScreen:
    def __init__(self, menu, image_name):

        # Lectura do ficheiro de configuracion
        parser = configparser.ConfigParser()
        parser.read("GaiaStation.config")

        self.menu = menu
        # Cárgase a imaxe de fondo
        self.image = ResourcesManager.load_image(image_name)
        self.image = pygame.transform.scale(self.image, (int(parser.get("director", "SCREEN_WIDTH")), int(parser.get("director", "SCREEN_HEIGHT"))))
        # Lista cos elementos da GUI
        self.GUI_elements = []
        # Lista cos elementos interactivos
        self.GUI_interactive_elements = []
        self.iterator = cycle(self.GUI_interactive_elements)
        self.selected = None

    def events(self, events_list):
        for event in events_list:
            if event.type == KEYDOWN:
                # Si la tecla es Escape
                if event.key == K_ESCAPE:
                    # Se sale del programa
                    pygame.quit()
                    sys.exit()
                elif event.key == K_UP:
                    self.selected.unselect(self)
                    for x in range(len(self.GUI_interactive_elements) - 1):
                        self.selected = next(self.iterator)
                    self.selected.select(self)
                elif event.key == K_DOWN:
                    self.selected.unselect(self)
                    self.selected = next(self.iterator)
                    self.selected.select(self)
                elif event.key == K_RETURN:
                    self.selected.action()
                elif isinstance(self.selected, SetVolumeText):
                    if event.key == K_LEFT:
                        self.selected.minus()
                        self.selected.select(self)
                    elif event.key == K_RIGHT:
                        self.selected.plus()
                        self.selected.select(self)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self, screen):
        # Primeiro debúxase a imaxe de fondo
        screen.blit(self.image, self.image.get_rect())
        # Despois debúxanse os botóns
        for element in self.GUI_elements:
            element.draw(screen)

#=======================================================================================

class GUIInitialScreen(GUIScreen):
    def __init__(self, menu):
        GUIScreen.__init__(self, menu, "portada.jpg")

        # Créase o texto e añádese á lista
        play_text = PlayText(self)
        exit_text = ExitText(self)
        title_text = TitleText(self)
        config_text = ConfigText(self)
        self.GUI_elements.append(title_text)
        self.GUI_elements.append(play_text)
        self.GUI_elements.append(config_text)
        self.GUI_elements.append(exit_text)

        #Tamén creamos unha lista cos elementos que queremos que sexan interactivos
        self.GUI_interactive_elements.append(play_text)
        self.GUI_interactive_elements.append(config_text)
        self.GUI_interactive_elements.append(exit_text)
        self.selected = self.GUI_interactive_elements[0]
        self.selected.select(self)

#=======================================================================================

class GUIConfigScreen(GUIScreen):
    def __init__(self, menu):
        GUIScreen.__init__(self, menu, "config.jpg")

        # Créase o texto e añádese á lista
        return_text = ReturnText(self)
        self.GUI_elements.append(return_text)
        volume_text = SetVolumeText(self)
        self.GUI_elements.append(volume_text)
        fullscreen_text = ToggleFullScreem(self)
        self.GUI_elements.append(fullscreen_text)

        #Tamén creamos unha lista cos elementos que queremos que sexan interactivos
        self.GUI_interactive_elements.append(return_text)
        self.GUI_interactive_elements.append(volume_text)
        self.GUI_interactive_elements.append(fullscreen_text)
        self.selected = self.GUI_interactive_elements[0]
        self.selected.select(self) # Para actualizar o print

# -------------------------------------------------
# Clase Menu, a escena

class Menu(Scene):

    def __init__(self, director):
        Scene.__init__(self, director)

        self.screens_list = []
        # Créase a pantalla e añádese á lista
        self.screens_list.append(GUIInitialScreen(self))
        ResourcesManager.load_music('menu.mp3')
        pygame.mixer.music.play(loops=-1)
        self.show_initial_screen()

    def update(self, *args):
        return

    def events(self, events_list):
        # Pásaselle a lista de eventos á pantalla actual
        self.screens_list[self.current_screen].events(events_list)

    def draw(self, screen):
        self.screens_list[self.current_screen].draw(screen)

    def exit_program(self):
        pygame.quit()
        sys.exit()

    def execute_game(self):
         level = Level1(self.director, 'level1.png', 'level1_obstacles.csv', None)
         self.director.stack_scene(level)

    def show_initial_screen(self):
        self.current_screen = 0

    def show_config_screen(self):
        self.screens_list.append(GUIConfigScreen(self))
        self.current_screen += 1

    def return_screen(self):
        self.screens_list.pop()
        self.current_screen = self.current_screen - 1
