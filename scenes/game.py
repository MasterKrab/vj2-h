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

from elements.bug import Enemy
from time import time


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def gameLoop(GAME_OVER, QUIT_GAME, skin: str):
    code = QUIT_GAME

    """iniciamos los modulos de pygame / skin tiene la ruta del asset a usar como skin de jorge"""

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('audio/gary.mp3')
    pygame.mixer.music.play(-1)
    hitmarker_sfx = pygame.mixer.Sound('audio/hitmarker.mp3')
    oof_sfx = pygame.mixer.Sound('audio/oof.mp3')
    
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
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, skin)

    """ 4.- contenedores de enemigos y jugador"""
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    """ hora de hacer el gameloop """
    # variable booleana para manejar el loop
    running = True

    ''' Sistema de puntacion'''
    player_score = 0
    score = pygame.font.SysFont("montserrat", 50)
    score = score.render(f"SCORE: {str(player_score)}", True, BLACK, WHITE)
    score_rect = score.get_rect(center=(100, 20))

    '''vidas'''
    lifes = 3
    hp = pygame.font.SysFont("montserrat", 50)
    hp = hp.render("VIDAS: " + str(lifes), True, BLACK, WHITE)
    hp_rect = hp.get_rect(center=(SCREEN_WIDTH - 100, 20))
    invulneravility_time = 0

    # loop principal del juego

    while running:

        screen.blit(background_image, [0, 0])
        screen.blit(score, score_rect)
        screen.blit(hp, hp_rect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # POR HACER (2.5): Pintar proyectiles en pantalla
        for projectile in player.projectiles:
            screen.blit(projectile.surf, projectile.rect)

        # POR HACER (2.5): Eliminar bug si colisiona con proyectil
        # pygame.sprite.groupcollide(enemies, player.projectiles, True, True)
        if pygame.sprite.groupcollide(enemies, player.projectiles, True, True):
            player_score += 100
            score = pygame.font.SysFont("montserrat", 50)
            score = score.render("SCORE: " + str(player_score), True, BLACK, WHITE)
            score_rect = score.get_rect(center=(100, 20))
            hitmarker_sfx.play()

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()

        if pygame.sprite.spritecollideany(player, enemies):
            if time() - invulneravility_time > 2:
                if lifes == 1:
                    player.kill()
                    code = GAME_OVER
                    oof_sfx.play()
                    running = False
                    
                else:
                    lifes -= 1
                    hp = pygame.font.SysFont("montserrat", 50)
                    hp = hp.render("VIDAS: " + str(lifes), True, BLACK, WHITE)
                    hp_rect = hp.get_rect(center=(SCREEN_WIDTH - 100, 20))
                    invulneravility_time = time()
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

            elif event.type == ADDENEMY:
                new_enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)


        clock.tick(40)

    pygame.mixer.music.stop()

    return code
