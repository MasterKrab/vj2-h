import pygame

from constants.colors import WHITE

from utils.timer import timer


def render_notifications(screen: pygame.Surface, messages: set[str]):
    font = pygame.font.SysFont("monserrat", 25, bold=True)

    for index, message in enumerate(messages):
        text = font.render(message, True, WHITE)
        rect = text.get_rect(
            center=(
                25 + text.get_width() / 2,
                screen.get_height() - text.get_height() * index - 25,
            )
        )

        screen.blit(text, rect)
