#!/usr/bin/env python2

import pygame
import sys
import time
from lib.Character import Character

class GameWorld:
	GAME_WIDTH = 640
	GAME_HEIGTH = 460
	GAME_DIMENSION = [GAME_WIDTH, GAME_HEIGTH]

	BACKGROUND_COLOR = pygame.Color(0,0,0);

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode(self.GAME_DIMENSION);
		self.player = Character(Character.CHARACTER_FISH);

	def start(self):
		jumpmode = False

		while 1:
			for e in pygame.event.get():
				if (e.type == pygame.QUIT):
					sys.exit(0);
				elif (e.type == pygame.KEYDOWN):
					if (e.key == 32):
						jumpmode = True

			if (jumpmode):
				jumpmode = self.player.jump();

			self.screen.fill(self.BACKGROUND_COLOR)
			self.screen.blit(self.player.character_image, self.player.character_rect)

			pygame.display.flip()
			time.sleep(1.0 / 30)