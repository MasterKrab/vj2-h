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

from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_SPACE

from constants.state import GAME_OVER, QUIT_GAME

from elements.jorge import Player
from elements.cursor import Cursor
from elements.enemies import Bug, BugBoss, Bullet, Bomb
from elements.powerups import PickablePowerUp
from components.pause_menu import show_pause
from components.notification import render_notifications

from utils.timer import timer


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700


NOTIFICATIONS_TIME = 5

ADD_BUG = pygame.USEREVENT + 1
ADD_BOSS_BUG = pygame.USEREVENT + 2
ADD_BULLET = pygame.USEREVENT + 3
ADD_POWERUP = pygame.USEREVENT + 4
ADD_BOMB = pygame.USEREVENT + 5


def set_timers(stop=False):
    if stop:
        pygame.time.set_timer(ADD_BUG, 0)
        pygame.time.set_timer(ADD_BULLET, 0)
        pygame.time.set_timer(ADD_POWERUP, 0)
        pygame.time.set_timer(ADD_BOSS_BUG, 0)
        pygame.time.set_timer(ADD_BOMB, 0)
        return

    pygame.time.set_timer(ADD_BUG, 1500)
    pygame.time.set_timer(ADD_BULLET, 5000)
    pygame.time.set_timer(ADD_POWERUP, 10000)
    pygame.time.set_timer(ADD_BOSS_BUG, 20000)
    pygame.time.set_timer(ADD_BOMB, 3500)


def gameLoop(skin: str, achievements: set):
    code = QUIT_GAME

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

    set_timers()

    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, skin)
    cursor = Cursor()

    enemies = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    """ hora de hacer el gameloop """
    # variable booleana para manejar el loop
    running = True
    paused = False

    """ Sistema de puntacion"""
    player_score = 0
    score_font = pygame.font.SysFont("montserrat", 30)

    """vidas"""
    health_font = pygame.font.SysFont("montserrat", 30)

    time_font = pygame.font.SysFont("montserrat", 50)

    start_time = timer.current
    game_time = 15

    notifications = set()

    kill_count = 0

    while running:

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = not paused

                    if paused:
                        timer.pause()
                    else:
                        timer.resume()
                        set_timers()

                if event.key == K_SPACE:
                    player.super_shoot()

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
            elif event.type == ADD_BOMB:
                new_bomb = Bomb(SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.add(new_bomb)
                all_sprites.add(new_bomb)

        if timer.is_paused:
            show_pause(screen)
            set_timers(stop=True)
            continue

        screen.blit(background_image, [0, 0])

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        for projectile in player.projectiles:
            screen.blit(projectile.surf, projectile.rect)

        for power_up in power_ups:
            if pygame.sprite.collide_rect(player, power_up):
                player.add_power_up(power_up.player_power_up)
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

            player_score += 10
            kill_count += 1

            for i in range(1, 5):
                if player_score < 10**i:
                    continue

                text = f"Logro: {10**i} puntos"

                if text in achievements:
                    continue

                achievements.add(text)
                notifications.add((text, timer.current))

            for count in [5, 10, 25, 50, 100, 500]:
                if kill_count < count:
                    continue

                text = f"Logro: {count} enemigos eliminados"

                if text in achievements:
                    continue

                achievements.add(text)
                notifications.add((text, timer.current))

            if isinstance(enemy, BugBoss):
                text = f"Logro: ¡Mataste a un Bug Jefe!"

                if text not in achievements:
                    achievements.add(text)
                    notifications.add((text, timer.current))

            game_time += 5

            hitmarker_sfx.play()

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()

        for power_up in power_ups:
            power_up.update()

        for enemy in enemies:
            if not pygame.sprite.collide_rect(enemy, player):
                continue

            if isinstance(enemy, Bomb) and not enemy.exploded:
                continue

            if isinstance(enemy, Bullet) and not enemy.exploded:
                enemy.damage()

            if not player.is_invulnerable:
                player.damage()

                if not player.is_alive:
                    code = GAME_OVER
                    oof_sfx.play()
                    running = False
                else:
                    oof_sfx.play()

        remaining_time = int(game_time - (timer.current - start_time))

        if remaining_time <= 0:
            code = GAME_OVER
            oof_sfx.play()
            running = False

        score_text = score_font.render(f"SCORE: {player_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(100, 20))

        time_text = time_font.render(str(remaining_time), True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH / 2, 20))

        health_text = health_font.render(
            f"VIDAS: {player.lives}",
            True,
            WHITE,
        )
        health_rect = health_text.get_rect(center=(SCREEN_WIDTH - 100, 20))

        for notification in list(notifications):
            if timer.current - notification[1] > NOTIFICATIONS_TIME:
                notifications.remove(notification)

        render_notifications(
            screen, [notification[0] for notification in notifications]
        )

        cursor.update(pygame.mouse.get_pos())

        screen.blit(cursor.surf, cursor.rect)
        screen.blit(score_text, score_rect)
        screen.blit(time_text, time_rect)
        screen.blit(health_text, health_rect)

        pygame.display.flip()

        clock.tick(40)

    pygame.mixer.music.stop()

    return code
