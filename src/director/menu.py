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
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Xogar', (380, 300))

    def select(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (138, 41, 10), 'Xogar', (380, 300))

    # Igual que o __init__, pero replícoo porque só son dúas líneas e ao chamar á función
    # enténdese mellor así o funcionamento
    def unselect(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Xogar', (380, 300))

    def action(self):
        self.screen.menu.execute_game()

class ConfigText(GUIText):
    def __init__(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Configuración', (330, 335))
    
    def select(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (138, 41, 10), 'Configuración', (330, 335))

    def unselect(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Configuración', (330, 335))

    def action(self):
        self.screen.menu.show_config_screen()

class ExitText(GUIText):
    def __init__(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Saír', (382, 370))

    def select(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (138, 41, 10), 'Saír', (382, 370))

    def unselect(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Saír', (382, 370))

    def action(self):
        self.screen.menu.exit_program()

class ReturnText(GUIText):
    def __init__(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Volver', (360, 240))

    def select(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (138, 41, 10), 'Volver', (360, 240))

    def unselect(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 26)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'Volver', (360, 240))

    def action(self):
        self.screen.menu.return_screen()

class TitleText(GUIText):
    def __init__(self, screen):
        font = ResourcesManager.loadFont("upheavtt.ttf", 52)
        GUIText.__init__(self, screen, font, (237, 82, 47), 'GAIA STATION', (260, 250))

# -------------------------------------------------
# Clase GUIScreen e as distintas pantallas

class GUIScreen:
    def __init__(self, menu, image_name):
        self.menu = menu
        # Cárgase a imaxe de fondo
        self.image = ResourcesManager.LoadImage(image_name)
        self.image = pygame.transform.scale(self.image, (800, 600))
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
                    self.selected = next(self.iterator)
                    self.selected = next(self.iterator)
                    self.selected.select(self)
                elif event.key == K_DOWN:
                    self.selected.unselect(self)
                    self.selected = next(self.iterator)
                    self.selected.select(self)
                elif event.key == K_RETURN:
                    self.selected.action()
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

        #Tamén creamos unha lista cos elementos que queremos que sexan interactivos
        self.GUI_interactive_elements.append(return_text)
        self.selected = self.GUI_interactive_elements[0]
        self.selected.select(self)

# -------------------------------------------------
# Clase Menu, a escena

class Menu(Scene):

    def __init__(self, director):
        Scene.__init__(self, director)

        self.screens_list = []
        # Créase a pantalla e añádese á lista
        self.screens_list.append(GUIInitialScreen(self))
        # ResourcesManager.loadMusic('level.mp3')
        # pygame.mixer.music.play(loops=-1)
        # pygame.mixer.music.stop()
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
         level = Level1(self.director, 'level1.png', 'level1_obstacles.csv')
         self.director.stack_scene(level)

    def show_initial_screen(self):
        self.current_screen = 0

    def show_config_screen(self):
        self.screens_list.append(GUIConfigScreen(self))
        self.current_screen += 1

    def return_screen(self):
        self.screens_list.pop()
        self.current_screen = self.current_screen - 1
