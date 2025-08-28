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

from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from elements.jorge import Player

from elements.bug import Enemy

from elements.cursor import Cursor

from scenes import game_over


def gameLoop(GAME_OVER, QUIT_GAME):
    code = QUIT_GAME

    """iniciamos los modulos de pygame"""

    pygame.init()

    """ Creamos y editamos la ventana de pygame (escena) """
    """ 1.-definir el tamaño de la ventana"""
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700

    """ 2.- crear el objeto pantalla"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load("assets/background.png").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    """ Preparamos el gameloop """
    """ 1.- creamos el reloj del juego"""

    clock = pygame.time.Clock()
    """ 2.- generador de enemigos"""

    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 600)

    """ 3.- creamos la instancia de jugador"""
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)

    """ 4.- contenedores de enemigos y jugador"""
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    """ hora de hacer el gameloop """
    # variable booleana para manejar el loop
    running = True

    # loop principal del juego

    cursor = Cursor()
    all_sprites.add(cursor)

    while running:

        screen.blit(background_image, [0, 0])

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # POR HACER (2.5): Pintar proyectiles en pantalla
        for projectile in player.projectiles:
            screen.blit(projectile.surf, projectile.rect)

        # POR HACER (2.5): Eliminar bug si colisiona con proyectil
        pygame.sprite.groupcollide(enemies, player.projectiles, True, True)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()

        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            code = GAME_OVER
            running = False

        pygame.display.flip()

        # iteramos sobre cada evento en la cola
        for event in pygame.event.get():
            # se presiono una tecla?
            if event.type == KEYDOWN:
                # era la tecla de escape? -> entonces terminamos
                if event.key == K_ESCAPE:
                    running = False

            # fue un click al cierre de la ventana? -> entonces terminamos
            elif event.type == QUIT:
                running = False

            elif event.type == ADDENEMY:
                new_enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            # POR HACER (2.4): Agregar evento disparo proyectil
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot(pygame.mouse.get_pos())

            elif event.type == pygame.MOUSEMOTION:
                cursor.update(*pygame.mouse.get_pos())

        clock.tick(40)

    return code
