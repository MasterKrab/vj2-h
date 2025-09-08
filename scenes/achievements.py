import pygame


from pygame.locals import KEYDOWN, K_SPACE, QUIT, K_ESCAPE

from constants.state import QUIT_GAME, MAIN_MENU

from constants.colors import WHITE

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700


def gameLoop(achievements: set):

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    background_image = pygame.image.load("assets/mainmenubackground.jpg").convert()
    background_image = pygame.transform.scale(
        background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    font_title = pygame.font.SysFont("monserrat", 60)
    font_subtext = pygame.font.SysFont("monserrat", 30)
    font_text = pygame.font.SysFont("monserrat", 25)

    while True:
        screen.blit(background_image, (0, 0))

        title_text = font_title.render("Logros", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 50))

        sub_text = font_subtext.render(
            "Presiona [ESPACIO] para volver a jugar o [ESC] para salir del juego",
            True,
            WHITE,
        )
        sub_text_rect = sub_text.get_rect(center=(SCREEN_WIDTH / 2, 100))

        screen.blit(title_text, title_rect)
        screen.blit(sub_text, sub_text_rect)

        for index, achievement in enumerate(achievements):
            text = font_text.render(achievement, True, WHITE)
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH / 2, 150 + index * (text.get_height() + 10))
            )
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return QUIT_GAME

                if event.key == K_SPACE:
                    return MAIN_MENU

            elif event.type == QUIT:
                return QUIT_GAME

        clock.tick(40)
