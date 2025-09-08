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
from pygame.locals import K_w, K_s, K_a, K_d, SRCALPHA

from utils.timer import timer

from elements.projectile import Projectile
from elements.powerups import CoolDownReduction, LifeUp, Shield, SpeedBoost

import math


COOLDOWN = 1
SUPER_COOLDOWN = 5


class Player(pygame.sprite.Sprite):
    MOVE_KEYS = {
        K_w: (0, -1),
        K_s: (0, 1),
        K_a: (-1, 0),
        K_d: (1, 0),
    }

    def __init__(self, screen_width, screen_height, skin: str):
        super(Player, self).__init__()

        self.size = 90

        self.surf = pygame.Surface((self.size, self.size))
        self.surf.set_colorkey((0, 0, 0, 0))

        self.projectile_sfx = pygame.mixer.Sound("audio/fire.mp3")
        self.super_projectile_sfx = pygame.mixer.Sound("audio/ballista.mp3")
        JorgePNG = pygame.image.load("assets/" + skin)
        self.avatar = pygame.transform.scale(JorgePNG, (self.size, self.size))
        self.avatar_surface = pygame.Surface((self.size, self.size), SRCALPHA)
        self.avatar_surface.blit(self.avatar, (0, 0))

        self.rect = self.surf.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.position = (screen_width // 4, screen_height // 2)
        self.rect.center = self.position

        self.last_shoot = timer.current
        self.last_super_shoot = timer.current
        self.power_ups = set()
        self.lives = 3
        self.last_damage_time = None
        self.normal_speed = 7

        self.projectiles = pygame.sprite.Group()

    @property
    def speed(self):
        for power_up in self.active_power_ups:
            if isinstance(power_up, SpeedBoost):
                return self.normal_speed * (1 + power_up.boost)

        return self.normal_speed

    @property
    def is_invulnerable(self):
        return (
            self.last_damage_time is not None
            and timer.current - self.last_damage_time < 3
        )

    @property
    def is_alive(self):
        return self.lives > 0

    @property
    def active_power_ups(self):

        for power_up in list(self.power_ups):
            if not power_up.is_active:
                self.power_ups.remove(power_up)

        return self.power_ups

    def add_power_up(self, power_up):
        if isinstance(power_up, LifeUp):
            self.lives += 1
            return

        self.power_ups.add(power_up)

    @property
    def shoot_cooldown(self):
        for power_up in self.active_power_ups:
            if isinstance(power_up, CoolDownReduction):
                return COOLDOWN * (1 - power_up.reduction)

        return COOLDOWN

    @property
    def super_shoot_cooldown(self):
        for power_up in self.active_power_ups:
            if isinstance(power_up, CoolDownReduction):
                return SUPER_COOLDOWN * (1 - power_up.reduction)

        return SUPER_COOLDOWN

    def damage(self):
        if self.is_invulnerable:
            return

        self.last_damage_time = timer.current

        for power_up in self.active_power_ups:
            if isinstance(power_up, Shield):
                self.power_ups.remove(power_up)
                return

        self.lives = max(0, self.lives - 1)

        if self.lives == 0:
            self.kill()

    def update(self, pressed_keys):
        self.surf.fill((0, 0, 0, 0))
        self.rect = self.surf.get_rect()

        for power_up in self.active_power_ups:
            if isinstance(power_up, Shield):
                shield_surface = power_up.get_surface(self.size)
                self.surf.blit(shield_surface, (0, 0))

        self.surf.blit(self.avatar_surface, (0, 0))

        for key in self.MOVE_KEYS:
            if pressed_keys[key]:
                delta_x, delta_y = self.MOVE_KEYS[key]

                new_x = max(
                    0,
                    min(self.position[0] + delta_x * self.speed, self.screen_width),
                )
                new_y = max(
                    0,
                    min(self.position[1] + delta_y * self.speed, self.screen_height),
                )

                self.position = (new_x, new_y)

        self.rect.center = self.position

        self.projectiles.update()

    def shoot_direction(self):
        cursor = pygame.mouse.get_pos()

        delta_x = cursor[0] - self.rect.centerx
        delta_y = cursor[1] - self.rect.centery
        magnitude = (delta_x**2 + delta_y**2) ** 0.5

        direction = (
            (delta_x / magnitude, delta_y / magnitude) if magnitude != 0 else (0, 0)
        )

        return direction

    def shoot(self):
        if self.last_shoot < 0 or timer.current - self.last_shoot < self.shoot_cooldown:
            return

        self.last_shoot = timer.current

        direction = self.shoot_direction()

        projectile = Projectile(
            self.rect.center, direction, self.screen_width, self.screen_height
        )
        self.projectiles.add(projectile)
        self.projectile_sfx.play()

    def super_shoot(self):
        if (
            self.last_super_shoot < 0
            or timer.current - self.last_super_shoot < self.super_shoot_cooldown
        ):
            return

        direction = self.shoot_direction()

        directions = []
        rotations = [5, -5, 20, -20, 30, -30]

        for angle in rotations:
            angle = math.atan2(direction[1], direction[0]) + math.radians(angle)
            directions.append((math.cos(angle), math.sin(angle)))

        projectiles = [
            Projectile(
                self.rect.center,
                direction,
                self.screen_width,
                self.screen_height,
                radius=120,
            )
            for direction in directions
        ]

        self.projectiles.add(*projectiles)
        self.projectile_sfx.play()
        self.last_super_shoot = timer.current
        self.super_projectile_sfx.play()
