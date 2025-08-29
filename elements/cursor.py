if __name__ == "__main__":  # Solo para que no ejecutes este archivo
    import sys

    print(
        "\033[38;2;255;0;0mESTE MODULO NO DEBE EJECUTARSE. EJECUTAR main.py\033[0m\n"
        * 3
    )
    sys.exit()

import pygame

from pygame.locals import RLEACCEL

CROSSHAIR_SIZE = 50

crosshair = pygame.image.load("assets/crosshair.png")
crosshair = pygame.transform.scale(crosshair, (CROSSHAIR_SIZE, CROSSHAIR_SIZE))


class Cursor(pygame.sprite.Sprite):

    def __init__(self):
        super(Cursor, self).__init__()

        self.surf = crosshair
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, position_x, position_y):
        self.rect = self.surf.get_rect(center=(position_x, position_y))
