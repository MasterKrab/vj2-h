if __name__ == "__main__":  # Solo para que no ejecutes este archivo
    import sys

    print(
        "\033[38;2;255;0;0mESTE MODULO NO DEBE EJECUTARSE. EJECUTAR main.py\033[0m\n"
        * 3
    )
    sys.exit()

import pygame
import math


class Projectile(pygame.sprite.Sprite):

    def __init__(self, pos, direction, SCREEN_WIDTH, SCREEN_HEIGHT, radius=50):
        super(Projectile, self).__init__()

        angle = math.atan2(direction[1], direction[0])
        angle_degrees = math.degrees(angle)

        projectile = pygame.image.load("assets/projectile.png")
        projectile = pygame.transform.rotate(
            pygame.transform.scale(projectile, (radius, 2 * radius)), -angle_degrees
        )
        self.surf = projectile
        self.rect = self.surf.get_rect(center=pos)

        self.speed = 10
        self.direction = direction
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

    def update(self):
        self.rect.move_ip(
            self.direction[0] * self.speed, self.direction[1] * self.speed
        )

        # Agregue unas tolerancias aca porque se me estaban bugeando los limites.
        if (
            self.rect.left < 0 - 100
            or self.rect.right > self.screen_width + 100
            or self.rect.top < 0 - 100
            or self.rect.bottom > self.screen_height + 100
        ):
            self.kill()
