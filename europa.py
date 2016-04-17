#!/usr/bin/env python2

from lib.GameWorld import GameWorld
from lib.Menu import Menu

GAME_WIDTH = 1280
GAME_HEIGHT = 800
GAME_DIMENSION = [GAME_WIDTH, GAME_HEIGHT]

menu = Menu(GAME_DIMENSION)
menu.start()

#game = GameWorld();
#game.start();
