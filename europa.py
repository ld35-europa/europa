#!/usr/bin/env python2

import sys

from lib.GameWorld import GameWorld
from lib.Menu import Menu

menu = Menu()
game = GameWorld(menu)
game.start()
