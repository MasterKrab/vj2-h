import pygame

import scenes.main_menu as MainMenu
import scenes.game as GameScene
import scenes.game_over as GameOver
import scenes.character_menu as CharacterMenu
import scenes.achievements as Achievements

from constants.state import ACHIEVEMENTS, MAIN_MENU, QUIT_GAME

from utils.timer import timer

import time
import random

random.seed(time.time() * time.time_ns())


achievements = set()

while True:
    pygame.init()
    timer.start_timer()

    while True:
        code = MainMenu.gameLoop()

        if code != ACHIEVEMENTS:
            break

        code = Achievements.gameLoop(achievements)

        if code == MAIN_MENU:
            continue

    if code == QUIT_GAME:
        break

    skin = CharacterMenu.gameLoop()

    if not skin:
        break

    code = GameScene.gameLoop(skin, achievements)

    if code == QUIT_GAME:
        break

    code = GameOver.gameLoop()

    if code == QUIT_GAME:
        break
