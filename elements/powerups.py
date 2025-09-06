import pygame
from abc import ABC
from time import time
from random import randint
from constants.colors import CYAN


class PowerUp(ABC):
    def __init__(self):
        self.duration = randint(5, 15)

        self.time = -1

    @property
    def is_active(self):
        if self.time == -1:
            return False

        return time() - self.time < self.duration

    def activate(self):
        self.time = time()


class CoolDownReduction(PowerUp):
    def __init__(self):
        super().__init__()
        self.reduction = randint(35, 50) / 100


class SpeedBoost(PowerUp):
    def __init__(self):
        super().__init__()
        self.boost = randint(20, 40) / 100


class Shield(PowerUp):
    def __init__(self):
        super().__init__()

        self.surface = pygame.Surface((0, 0), pygame.SRCALPHA)

    def get_surface(self, size: int):
        self.surface = pygame.transform.scale(self.surface, (size, size))

        pygame.draw.circle(
            self.surface, (*CYAN, 180), (size // 2, size // 2), size // 2
        )

        return self.surface


def get_random_power_up():
    power_ups = [CoolDownReduction, SpeedBoost, Shield]
    return power_ups[randint(0, len(power_ups) - 1)]()


class PickablePowerUp(pygame.sprite.Sprite):
    def __init__(self, screen_width: int, screen_height: int):
        super(PickablePowerUp, self).__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.player_power_up = get_random_power_up()

        self.icon = pygame.image.load(
            f"assets/power_ups/{self.player_power_up.__class__.__name__}.png"
        )
        self.surf = pygame.transform.scale(self.icon, (40, 40))
        self.rect = self.surf.get_rect()

        self.speed = 10

        if randint(0, 1):
            self.rect.center = (0, randint(0, self.screen_height))
        else:
            self.rect.center = (self.screen_width, randint(0, self.screen_height))
            self.speed *= -1

    def update(self):
        self.rect.move_ip(self.speed, 0)

        if self.rect.right < 0 or self.rect.left > self.screen_width:
            self.kill()
