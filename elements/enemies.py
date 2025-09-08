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

from utils.timer import timer


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


class EnemyFollowPlayer:
    def __init__(self, player, acceleration=2, max_velocity=7):
        self.player = player

        self.velocity = (0, 0)
        self.max_velocity = max_velocity
        self.acceleration = acceleration

    def update(self):
        player_position = self.player.rect.center

        distance_x = player_position[0] - self.rect.centerx
        distance_y = player_position[1] - self.rect.centery

        distance = math.sqrt(distance_x**2 + distance_y**2)

        velocity_x = self.velocity[0] + (distance_x / distance) * self.acceleration
        velocity_y = self.velocity[1] + (distance_y / distance) * self.acceleration

        self.velocity = (
            max(-self.max_velocity, min(self.max_velocity, velocity_x)),
            max(-self.max_velocity, min(self.max_velocity, velocity_y)),
        )

        angle = math.atan2(-self.velocity[1], self.velocity[0])
        angle_degrees = math.degrees(angle)

        self.rect.move_ip(self.velocity)
        self.surf = pygame.transform.rotate(self.original_surf, angle_degrees)


class BugBoss(EnemyFollowPlayer, Bug):
    def __init__(self, player, screen_width, screen_height):
        Bug.__init__(self, screen_width, screen_height)
        EnemyFollowPlayer.__init__(self, player, acceleration=0.2, max_velocity=5)

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

        self.health = 10

    def damage(self):
        self.health -= 1

        if self.health <= 0:
            self.kill()


class Bullet(EnemyFollowPlayer, pygame.sprite.Sprite):
    bullet = pygame.image.load("assets/bullet.png")
    boom = pygame.image.load("assets/boom.png")

    def __init__(self, player, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        EnemyFollowPlayer.__init__(self, player, acceleration=1.25)

        self.boom_sound = pygame.mixer.Sound("audio/boom2.mp3")

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

        self.exploded = False
        self.explosion_start = None
        self.boom_time = 1

    def update(self):
        if not self.exploded:
            EnemyFollowPlayer.update(self)

        if self.exploded and timer.current - self.explosion_start > self.boom_time:
            self.kill()

    def damage(self):
        self.boom_sound.play()

        self.surf = pygame.transform.scale(self.boom, (80, 80))
        self.rect = self.surf.get_rect(center=self.rect.center)

        self.exploded = True
        self.explosion_start = timer.current


class Bomb(pygame.sprite.Sprite):
    bomb = pygame.image.load("assets/bomb.png")
    boom = pygame.image.load("assets/boom.png")

    def __init__(self, screen_width, screen_height):
        super(Bomb, self).__init__()

        self.boom_sound = pygame.mixer.Sound("audio/boom.mp3")

        self.surf = pygame.transform.scale(self.bomb, (100, 100))

        self.rect = self.surf.get_rect(
            center=(
                random.randint(100, screen_width - 100),
                -100,
            )
        )

        self.explode_at = random.randint(150, screen_height - 150)

        self.start_time = timer.current
        self.boom_time = 1
        self.explosion_start = None
        self.exploded = False
        self.speed = 5

    def explode(self):
        self.surf = pygame.transform.scale(self.boom, (100, 100))
        self.rect = self.surf.get_rect(center=self.rect.center)

        self.exploded = True
        self.explosion_start = timer.current
        self.boom_sound.play()

    def update(self):
        if not self.exploded:
            self.rect.move_ip((0, self.speed))

        if not self.exploded and self.rect.centery >= self.explode_at:
            self.explode()

        if self.exploded and timer.current - self.explosion_start > self.boom_time:
            self.kill()

    def damage(self):
        self.explode()
