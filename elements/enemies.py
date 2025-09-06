"""
Hola este es modulo Bug,
este modulo manejara la creacion y acciones de los Bugs
"""

if __name__ == "__main__":  # Solo para que no ejecutes este archivo
    import sys

    print(
        "\033[38;2;255;0;0mESTE MODULO NO DEBE EJECUTARSE. EJECUTAR main.py\033[0m\n"
        * 3
    )
    sys.exit()

import pygame
import random
import math
from pygame.locals import RLEACCEL


BUGpng = pygame.image.load("assets/bug.png")


class Bug(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super(Bug, self).__init__()
        self.surf = pygame.transform.scale(BUGpng, (64, 64))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                screen_width + 100,
                random.randint(0, screen_height),
            )
        )
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def damage(self):
        self.kill()


class BugBoss(Bug):
    def __init__(self, player, screen_width, screen_height):
        super(BugBoss, self).__init__(screen_width, screen_height)

        self.player = player

        self.original_surf = pygame.transform.rotate(
            pygame.transform.scale(BUGpng, (200, 200)), -180
        )

        self.surf = self.original_surf

        self.rect = self.surf.get_rect(
            center=(
                screen_width + 100,
                random.randint(0, screen_height),
            )
        )

        self.health = 5
        self.speed = 4

    def update(self):
        player_position = self.player.rect.center

        distance_x = player_position[0] - self.rect.centerx
        distance_y = player_position[1] - self.rect.centery

        distance = math.sqrt(distance_x**2 + distance_y**2)

        delta_x = max(-1, min(1, distance_x / distance) if distance != 0 else 0)
        delta_y = max(-1, min(1, distance_y / distance) if distance != 0 else 0)

        angle = math.atan2(-distance_y, distance_x)
        angle_degrees = math.degrees(angle)

        self.rect.move_ip(delta_x * self.speed, delta_y * self.speed)
        self.surf = pygame.transform.rotate(self.original_surf, angle_degrees)

    def damage(self):
        self.health -= 1

        if self.health <= 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    bullet = pygame.image.load("assets/bullet.png")

    def __init__(self, player, screen_width, screen_height):
        super(Bullet, self).__init__()

        self.player = player

        self.original_surf = pygame.transform.rotate(
            pygame.transform.scale(self.bullet, (80, 80)), -180
        )
        self.surf = self.original_surf

        self.rect = self.surf.get_rect(
            center=(
                screen_width + 100,
                random.randint(0, screen_height),
            )
        )

        self.speed = 8

    def update(self):
        if self.rect.colliderect(self.player.rect):
            self.kill()

        player_position = self.player.rect.center

        distance_x = player_position[0] - self.rect.centerx
        distance_y = player_position[1] - self.rect.centery

        distance = math.sqrt(distance_x**2 + distance_y**2)

        delta_x = max(-1, min(1, distance_x / distance) if distance != 0 else 0)
        delta_y = max(-1, min(1, distance_y / distance) if distance != 0 else 0)

        angle = math.atan2(-distance_y, distance_x)
        angle_degrees = math.degrees(angle)

        self.rect.move_ip(delta_x * self.speed, delta_y * self.speed)
        self.surf = pygame.transform.rotate(self.original_surf, angle_degrees)

    def damage(self):
        self.kill()
