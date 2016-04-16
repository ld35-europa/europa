#!/usr/bin/env python2

import pygame
import sys
import time
from random import random

from lib.Character import Character
from lib.Colors import Colors
from lib.Obstacle import Obstacle

class GameWorld:
	GAME_WIDTH = 1280
	GAME_HEIGHT = 800
	GAME_DIMENSION = [GAME_WIDTH, GAME_HEIGHT]

	OBSTACLE_MIN_HEIGHT = 125
	OBSTACLE_MAX_HEIGHT = 425
	OBSTACLE_MIN_WIDTH = 100
	OBSTACLE_MAX_WIDTH = 400

	BACKGROUND_COLOR = Colors.BLACK;

	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Europa')
		
		self.screen = pygame.display.set_mode(self.GAME_DIMENSION);
		self.player = Character();

	def start(self):
		self.generateObstacles();

		while 1:
			for e in pygame.event.get():
				if (e.type == pygame.QUIT):
					sys.exit(0);
				elif (e.type == pygame.KEYDOWN):
					if (e.key == 32 and self.player.state == self.player.CHARACTER_STATE_ALIVE and self.player.mode != self.player.MODE_JUMP):
						self.player.startJump()
					if (e.key == pygame.K_ESCAPE):
						sys.exit(0)
					if (e.key == pygame.K_1):
						self.player.startDie();

			self.player.drawOnSurface(self.screen);
			pygame.display.flip()
			time.sleep(1.0 / 30)

	def generateObstacles(self):
		x = 0
		obstacle = Obstacle()

		while (x < self.GAME_WIDTH):
			xdelta = int(random() * 400)
			xdelta = min(150, xdelta)
			x += xdelta
			w = max(self.OBSTACLE_MIN_WIDTH, int(random() * self.OBSTACLE_MAX_WIDTH))
			h = max(self.OBSTACLE_MIN_HEIGHT, int(random() * self.OBSTACLE_MAX_HEIGHT))

			self.screen.blit(obstacle.get_surface(w, h), (x, self.GAME_HEIGHT-h))
			x += w
