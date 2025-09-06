"""
Hola este es modulo game,
este modulo manejara la escena donde ocurre nuestro juego
"""

if __name__ == "__main__":  # Solo para que no ejecutes este archivo
    import sys

    print(
        "\033[38;2;255;0;0mESTE MODULO NO DEBE EJECUTARSE. EJECUTAR main.py\033[0m\n"
        * 3
    )
    sys.exit()

import pygame

from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_SPACE, K_RETURN

from elements.jorge import Player
from elements.enemies import Bug, BugBoss, Bullet
from elements.powerups import PickablePowerUp

from time import time


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700


ADD_BUG = pygame.USEREVENT + 1
ADD_BOSS_BUG = pygame.USEREVENT + 2
ADD_BULLET = pygame.USEREVENT + 3
ADD_POWERUP = pygame.USEREVENT + 4


def gameLoop(GAME_OVER, QUIT_GAME, skin: str):
    code = QUIT_GAME

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("audio/gary.mp3")
    pygame.mixer.music.play(-1)
    hitmarker_sfx = pygame.mixer.Sound("audio/hitmarker.mp3")
    oof_sfx = pygame.mixer.Sound("audio/oof.mp3")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load("assets/background.png").convert()
    background_image = pygame.transform.scale(
        background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    clock = pygame.time.Clock()

    pygame.time.set_timer(ADD_BUG, 1500)
    pygame.time.set_timer(ADD_BULLET, 5000)
    pygame.time.set_timer(ADD_POWERUP, 10000)
    pygame.time.set_timer(ADD_BOSS_BUG, 20000)

    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, skin)

    enemies = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    """ hora de hacer el gameloop """
    # variable booleana para manejar el loop
    running = True

    """ Sistema de puntacion"""
    player_score = 0
    score = pygame.font.SysFont("montserrat", 50)
    score = score.render(f"SCORE: {str(player_score)}", True, BLACK, WHITE)
    score_rect = score.get_rect(center=(100, 20))

    """vidas"""
    health_font = pygame.font.SysFont("montserrat", 50)
    health = health_font.render(f"VIDAS: {str(player.lives)}", True, BLACK, WHITE)
    health_rect = health.get_rect(center=(SCREEN_WIDTH - 100, 20))

    while running:
        screen.blit(background_image, [0, 0])
        screen.blit(score, score_rect)
        screen.blit(health, health_rect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # POR HACER (2.5): Pintar proyectiles en pantalla
        for projectile in player.projectiles:
            screen.blit(projectile.surf, projectile.rect)

        for power_up in power_ups:
            if pygame.sprite.collide_rect(player, power_up):
                player.power_ups.append(power_up.player_power_up)
                power_up.player_power_up.activate()
                power_ups.remove(power_up)
                all_sprites.remove(power_up)
            else:
                screen.blit(power_up.surf, power_up.rect)

        # POR HACER (2.5): Eliminar bug si colisiona con proyectil
        # pygame.sprite.groupcollide(enemies, player.projectiles, True, True)
        for enemy in enemies:

            projectile_hit = pygame.sprite.spritecollideany(enemy, player.projectiles)

            if not projectile_hit:
                continue

            projectile_hit.kill()
            player.projectiles.remove(projectile_hit)
            enemy.damage()

            if enemy.alive():
                continue

            player_score += 100
            score = pygame.font.SysFont("montserrat", 50)
            score = score.render("SCORE: " + str(player_score), True, BLACK, WHITE)
            score_rect = score.get_rect(center=(100, 20))
            hitmarker_sfx.play()

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()

        for power_up in power_ups:
            power_up.update()

        if pygame.sprite.spritecollideany(player, enemies):
            if not player.is_invulnerable:
                player.damage()

                if not player.is_alive:
                    code = GAME_OVER
                    oof_sfx.play()
                    running = False
                else:
                    health = health_font.render(
                        "VIDAS: " + str(player.lives), True, BLACK, WHITE
                    )
                    health_rect = health.get_rect(center=(SCREEN_WIDTH - 100, 20))
                    oof_sfx.play()

        pygame.display.flip()

        # iteramos sobre cada evento en la cola
        for event in pygame.event.get():
            # se presiono una tecla?
            if event.type == KEYDOWN:
                # era la tecla de escape? -> entonces terminamos
                if event.key == K_ESCAPE:
                    if paused:
                        running = False
                    else:
                        paused = True
                if event.key == K_SPACE:
                    player.shoot()

                if event.key == K_RETURN:
                    player.super_shoot()

            # fue un click al cierre de la ventana? -> entonces terminamos
            elif event.type == QUIT:
                running = False

            elif event.type == ADD_BUG:
                new_bug = Bug(SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.add(new_bug)
                all_sprites.add(new_bug)
            elif event.type == ADD_BOSS_BUG:
                new_boss = BugBoss(player, SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.add(new_boss)
                all_sprites.add(new_boss)
            elif event.type == ADD_BULLET:
                new_bullet = Bullet(player, SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.add(new_bullet)
                all_sprites.add(new_bullet)
            elif event.type == ADD_POWERUP:
                new_powerup = PickablePowerUp(SCREEN_WIDTH, SCREEN_HEIGHT)
                power_ups.add(new_powerup)
                all_sprites.add(new_powerup)

        clock.tick(40)

    pygame.mixer.music.stop()

    return code
