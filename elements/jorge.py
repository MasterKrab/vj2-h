"""
Hola este es modulo Jorge,
este modulo manejara la creacion y movimiento de Jorge
"""

if __name__ == "__main__":  # Solo para que no ejecutes este archivo
    import sys

    print(
        "\033[38;2;255;0;0mESTE MODULO NO DEBE EJECUTARSE. EJECUTAR main.py\033[0m\n"
        * 3
    )
    sys.exit()

import pygame
from pygame.locals import K_w, K_s, K_a, K_d, RLEACCEL 
from time import time

from elements.projectile import Projectile


COOLDOWN = 2


class Player(pygame.sprite.Sprite):

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, skin: str):
        self.projectile_sfx = pygame.mixer.Sound('audio/fire.mp3')
        super(Player, self).__init__()
        JorgePNG = pygame.image.load("assets/" + skin)
        JorgePNG_scaled = pygame.transform.scale(JorgePNG, (80, 80))
        self.surf = JorgePNG_scaled
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.last_shoot = time() - COOLDOWN

        # POR HACER (2.3): Crear lista de proyectiles
        self.projectiles = pygame.sprite.Group()

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -4)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 4)
        if pressed_keys[K_a]:
            self.rect.move_ip(-4, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(4, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

        # POR HACER (2.3): Actualizar la posición de los proyectiles
        self.projectiles.update()

    def shoot(self):
        if time() - self.last_shoot < COOLDOWN:
            return

        self.last_shoot = time()

        # POR HACER (2.3): Crear y calcular dirección proyectil
        direction = (1, 0)

        projectile = Projectile(
            self.rect.center, direction, self.screen_width, self.screen_height
        )
        self.projectiles.add(projectile)
        self.projectile_sfx.play()
