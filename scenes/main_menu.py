"""
Hola este es modulo menu principal.
"""

import pygame

from pygame.locals import KEYDOWN, K_RETURN, QUIT, K_ESCAPE


RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK= (255,19,255)


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
    background_image = pygame.image.load("assets/mainmenubackground.jpg").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    """ Texto """
    font_title = pygame.font.SysFont("monserrat", 111, bold=True)
    title = font_title.render("JORGE-WAVE", True, PINK)
    title_rect = title.get_rect(center=(500, SCREEN_HEIGHT /2 - 250))

    font_title2 = pygame.font.SysFont("monserrat", 110, bold=False)
    title2 = font_title2.render("JORGE-WAVE", True, WHITE)
    title_rect2 = title2.get_rect(center=(500+1, SCREEN_HEIGHT /2 - 250))

    #########################

    font_text = pygame.font.SysFont("monserrat", 40)
    text = font_text.render(
        "[ENTER] Jugar",
        True,
        WHITE
    )
    text_rect = text.get_rect(center=(500, (SCREEN_HEIGHT / 2) - 75))

    font_head = pygame.font.SysFont("monserrat", 45)
    head = font_head.render('Menú Principal:', True, WHITE)
    head_rect = head.get_rect(center=(500, (SCREEN_HEIGHT / 2) - 150))

    font_text1 = pygame.font.SysFont("monserrat", 40)
    text1 = font_text1.render(
        "[ESC] Salir del juego",
        True,
        WHITE
    )
    text_rect1 = text1.get_rect(center=(500, (SCREEN_HEIGHT / 2) + 300))

    """ hora de hacer el gameloop """
    # variable booleana para manejar el loop
    running = True

    # loop principal del juego

    while running:
        
        pygame.display.flip()
        screen.blit(background_image, [0, 0])
        screen.blit(title, title_rect)
        screen.blit(title2, title_rect2)
        screen.blit(text, text_rect)
        screen.blit(text1, text_rect1)
        screen.blit(head, head_rect)
        
        
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
