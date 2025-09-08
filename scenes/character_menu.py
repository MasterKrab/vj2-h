"""
Hola este es modulo menu principal.
"""

import pygame

from pygame.locals import KEYDOWN, K_RETURN, QUIT, K_1, K_2, K_3, K_4, K_5


RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 19, 255)


CHARACTERS = (
    ("Jorge Wave", "JorgeVJ.png"),
    ("Jorge Default", "Jorge_default.png"),
    ("Jorge Sombrero", "Jorge_sombrero.png"),
    ("Lakitu", "lakitu.png"),
    ("Kamek", "kamek.png"),
    ("Conker", "conker.png"),
)


def gameLoop():
    """iniciamos los modulos de pygame"""

    pygame.init()
    pygame.mixer.init()

    sound = pygame.mixer.Sound("audio/choose-your-character.mp3")
    sound.play()

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
    background_image = pygame.transform.scale(
        background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    """ Texto """
    font_title = pygame.font.SysFont("monserrat", 111, bold=True)
    title = font_title.render("ESCOGE TU LUCHADOR!", True, PINK)
    title_rect = title.get_rect(center=(500, SCREEN_HEIGHT / 2 - 250))

    font_title2 = pygame.font.SysFont("monserrat", 110, bold=False)
    title2 = font_title2.render("ESCOGE TU LUCHADOR!", True, WHITE)
    title_rect2 = title2.get_rect(center=(500 + 1, SCREEN_HEIGHT / 2 - 250))

    #########################

    font_text = pygame.font.SysFont("monserrat", 30)

    """ hora de hacer el gameloop """
    # variable booleana para manejar el loop
    running = True

    # loop principal del juego

    while running:

        pygame.display.flip()
        screen.blit(background_image, [0, 0])
        screen.blit(title, title_rect)
        screen.blit(title2, title_rect2)

        for i, (name, file) in enumerate(CHARACTERS):
            height = 100 + (i // 3) * 200

            position_x = 300 + (i % 3) * 250
            position_y = 100 + height

            text = font_text.render(f"[{i + 1}] {name}", True, WHITE)
            text_rect = text.get_rect(center=(position_x, position_y))

            image = pygame.image.load(f"assets/{file}").convert_alpha()
            image = pygame.transform.scale(image, (100, 100))
            image_rect = image.get_rect(center=(position_x, position_y + 100))

            screen.blit(text, text_rect)
            screen.blit(image, image_rect)

        # iteramos sobre cada evento en la cola
        for event in pygame.event.get():
            # se presiono una tecla?
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pygame.mixer.music.stop()
                    return ""

                for i in range(len(CHARACTERS)):
                    if event.key == K_1 + i:
                        pygame.mixer.music.stop()
                        return CHARACTERS[i][1]

            if event.type == QUIT:
                return ""

        clock.tick(40)
