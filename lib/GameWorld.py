#!/usr/bin/env python2

import pygame
import sys
import time
from lib.Character import Character
from lib.Colors import Colors
from lib.Obstacle import Obstacle

class GameWorld:
	GAME_WIDTH = 640
	GAME_HEIGHT = 480
	GAME_DIMENSION = [GAME_WIDTH, GAME_HEIGHT]

	BACKGROUND_COLOR = Colors.BLACK;

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode(self.GAME_DIMENSION);
		self.player = Character(Character.CHARACTER_FISH, self.screen);

	def start(self):
		self.generateObstacles();

		while 1:
			for e in pygame.event.get():
				if (e.type == pygame.QUIT):
					sys.exit(0);
				elif (e.type == pygame.KEYDOWN):
					if (e.key == 32):
						self.player.startJump()
					if (e.key == 27):
						sys.exit(0)

			self.player.move();
			pygame.display.flip()
			time.sleep(1.0 / 30)

	def generateObstacles(self):
		obstacle = Obstacle(200, 300)
		self.screen.blit(obstacle.get(), (150, self.GAME_HEIGHT-300))
