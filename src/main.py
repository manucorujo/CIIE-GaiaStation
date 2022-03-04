from tiles import *
from spritesheet import Spritesheet
import configparser


def main():

    ############################ LECTURA DO FICHEIRO DE CONFIGURACIÓN ###############################
    parser = configparser.ConfigParser()
    parser.read("GaiaStation.config")

    ################################ CARGA DA VENTÁ BÁSICA E  RELOXO ###############################
    pygame.init()
    DISPLAY_W, DISPLAY_H = int(parser.get("config", "DISPLAY_W")), int(parser.get("config", "DISPLAY_H")) 
    canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
    window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
    running = True
    clock = pygame.time.Clock()

    ################################# CARGA DO XOGADOR E TILESET ###################################
    spritesheet = Spritesheet(parser.get("config", "TILESET"))

    #################################### CARGA DO NIVEL #######################################
    map = TileMap(parser.get("config", "LEVEL1"), spritesheet )

    ################################# LOOP DO XOGO ##########################
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pass

        ####################################### ACTUALIZACIÓN ######################################
        canvas.fill((0, 0, 0))
        map.draw_map(canvas)
        window.blit(canvas, (0,0))
        pygame.display.update()

if __name__ == "__main__":
    main()









