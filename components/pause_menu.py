import pygame

from constants.colors import WHITE


def show_pause(screen: pygame.Surface):
    font = pygame.font.SysFont("monserrat", 60, bold=True)
    title = font.render("Pausa", True, WHITE)
    subtitle = font.render("Presiona [ESC] para seguir jugando", True, WHITE)
    title_rect = title.get_rect(
        center=((screen.get_width() / 2), (screen.get_height() / 2) - 25)
    )
    subtitle_rect = subtitle.get_rect(
        center=((screen.get_width() / 2), (screen.get_height() / 2) + 25)
    )

    screen.blit(title, title_rect)
    screen.blit(subtitle, subtitle_rect)
    pygame.display.flip()
