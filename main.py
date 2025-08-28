"""
Hola este es modulo principal,
el codigo que al ejecutar pondra en marcha nuestro juego
"""
import scenes.main_menu as MainMenu
import scenes.game as GameScene
import scenes.game_over as GameOver

GAME_OVER = 0
QUIT_GAME = 1
CONTINUE_GAME = 2

"""Inicio la escena de mi juego"""
while True:
    
    code = MainMenu.gameLoop(CONTINUE_GAME, QUIT_GAME) 
    
    if code == QUIT_GAME:
        break

    code = GameScene.gameLoop(GAME_OVER, QUIT_GAME)

    if code == QUIT_GAME:
        break

    code = GameOver.gameLoop(CONTINUE_GAME, QUIT_GAME)

    if code == QUIT_GAME:
        break

