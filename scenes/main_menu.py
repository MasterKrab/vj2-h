"""
Hola este es modulo menu principal.
"""

import pygame

from pygame.locals import KEYDOWN, K_RETURN, QUIT, K_ESCAPE


RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def gameLoop(CONTINUE_GAME, QUIT_GAME):
    """iniciamos los modulos de pygame"""

    pygame.init()

    """ Creamos y editamos la ventana de pygame (escena) """
    """ 1.-definir el tamaño de la ventana"""
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700

    """ 2.- crear el objeto pantalla"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    """ Preparamos el gameloop """
    """ 1.- creamos el reloj del juego"""

    clock = pygame.time.Clock()


    """ Fondo del menu"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load("assets/duck_wp.png").convert()

    """ Texto """
    font_title = pygame.font.SysFont("arial", 50)
    title = font_title.render("Menú Principal", True, RED, BLACK)
    title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    font_text = pygame.font.SysFont("arial", 20)
    text = font_text.render(
        "Presiona [ENTER] para jugar o [ESC] para salir del juego",
        True,
        WHITE,
        BLACK,
    )
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 100))

    """ hora de hacer el gameloop """
    # variable booleana para manejar el loop
    running = True

    # loop principal del juego

    while running:
        
        pygame.display.flip()
        screen.blit(background_image, [0, 0])
        screen.blit(title, title_rect)
        screen.blit(text, text_rect)
        
        
        # iteramos sobre cada evento en la cola
        for event in pygame.event.get():
            # se presiono una tecla?
            if event.type == KEYDOWN:
                # era la tecla de escape? -> entonces terminamos
                if event.key == K_ESCAPE:
                    return QUIT_GAME

                if event.key == K_RETURN:
                    return CONTINUE_GAME

            # fue un click al cierre de la ventana? -> entonces terminamos
            elif event.type == QUIT:
                return QUIT_GAME

        clock.tick(40)
