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
	GAME_FPS = 120;
	ANIMATION_FPS = GAME_FPS / 3;

	OBSTACLE_MIN_HEIGHT = 50
	OBSTACLE_MAX_HEIGHT = 125
	OBSTACLE_MIN_WIDTH = 50
	OBSTACLE_MAX_WIDTH = 200

	STATE_PLAYING = 0
	STATE_PAUSED = 1
	STATE_FINISHED = 2
	STATE_MENU = 3

	state = STATE_FINISHED

	BACKGROUND_COLOR = Colors.BLACK;

	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Europa')

		self.screen = pygame.display.set_mode(self.GAME_DIMENSION);
		self.player = Character();
		self.clock  = pygame.time.Clock();

	def update(self):
		self.player.update();
		if (self.player.checkCollision(self.obstacles) == True):
			self.player.startAnimationDeath();

	def draw(self):
		self.player.draw(self.screen);

	def start(self):
		self.generateObstacles();
		self.state = self.STATE_PLAYING;

		while self.state != self.STATE_FINISHED:
			self.clock.tick(self.GAME_FPS);
			for e in pygame.event.get():
				if (e.type == pygame.QUIT):
					self.state = self.STATE_FINISHED
					sys.exit(0);
				elif (e.type == pygame.KEYDOWN):
					if (\
						e.key == 32 and \
						self.player.state == self.player.CHARACTER_STATE_ALIVE and \
						self.player.action != self.player.ACTION_JUMP \
					):
						self.player.startJump()
					if (e.key == pygame.K_ESCAPE):
						sys.exit(0)
					if (e.key == pygame.K_1):
						self.player.startAnimationDeath();
					if (e.key == pygame.K_2):
						self.player.startAnimationTransform(self.player.ANIMATION_TRANSFORM_TO_FIRE)
					if (e.key == pygame.K_3):
						self.player.startAnimationTransform(self.player.ANIMATION_TRANSFORM_TO_WATER)

			self.update();
			self.draw();

			pygame.display.flip()

	def generateObstacles(self):
		self.obstacles = pygame.sprite.Group();
		w = max(self.OBSTACLE_MIN_WIDTH, int(random() * self.OBSTACLE_MAX_WIDTH))
		h = max(self.OBSTACLE_MIN_HEIGHT, int(random() * self.OBSTACLE_MAX_HEIGHT))

		x = 200
		while (x < self.GAME_WIDTH):
			xdelta = int(random() * 400)
			xdelta = min(150, xdelta)
			x += xdelta
			w = max(self.OBSTACLE_MIN_WIDTH, int(random() * self.OBSTACLE_MAX_WIDTH))
			h = max(self.OBSTACLE_MIN_HEIGHT, int(random() * self.OBSTACLE_MAX_HEIGHT))

			obstacle = Obstacle(w, h);
			obstacle.draw(self.screen, x);
			self.obstacles.add(obstacle)
