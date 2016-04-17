#!/usr/bin/env python2

# Start game with initializing the menu. If `-d` passed, start
# game directly

import sys

from lib.GameWorld import GameWorld
from lib.Menu import Menu

if (len(sys.argv) >= 2 and sys.argv[1] == "-d"):
	game = GameWorld()
	game.start()
else:
	menu = Menu(GameWorld.GAME_DIMENSION)
	menu.start()
