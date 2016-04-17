#!/usr/bin/env python2

# Start game with initializing the menu. If `-d` passed, start
# game directly

import sys

from lib.GameWorld import GameWorld
from lib.Menu import Menu

menu = Menu()
game = GameWorld(menu)
game.start()
#if (len(sys.argv) >= 2 and sys.argv[1] == "-d"):

#else:
	#game.startMenu()
