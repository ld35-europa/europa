#!/usr/bin/env python2

import pygame
import sys
import time
from lib.Character import Character
from lib.Colors import Colors
from lib.Wall import Wall

class GameWorld:
	GAME_WIDTH = 640
	GAME_HEIGTH = 460
	GAME_DIMENSION = [GAME_WIDTH, GAME_HEIGTH]

	BACKGROUND_COLOR = Colors.BLACK;

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode(self.GAME_DIMENSION);
		self.player = Character(Character.CHARACTER_FISH, self.screen);

	def start(self):
		while 1:
			for e in pygame.event.get():
				if (e.type == pygame.QUIT):
					sys.exit(0);
				elif (e.type == pygame.KEYDOWN):
					if (e.key == 32):
						self.player.startJump();

			self.screen.fill(self.BACKGROUND_COLOR)
			self.player.move();
			Wall(200, 300, 150, self.GAME_HEIGTH-300).drawOnScreen(self.screen);
			pygame.display.flip()
			time.sleep(1.0 / 30)