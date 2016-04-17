#!/usr/bin/env python2

import pygame
import sys
import time

from random import random
from pygame import Surface
from pygame import Rect

from lib.Character import Character
from lib.Colors import Colors
from lib.Obstacle import Obstacle

class GameWorld:
	GAME_WIDTH = 1280
	GAME_HEIGHT = 800
	GAME_DIMENSION = [GAME_WIDTH, GAME_HEIGHT]
	GAME_VELOCITY = 1;

	BUF_WIDTH = GAME_WIDTH*2
	BUF_HEIGHT = GAME_HEIGHT
	GAME_FPS = 120;
	ANIMATION_FPS = GAME_FPS / 3;

	OBSTACLE_MIN_HEIGHT = 125
	OBSTACLE_MAX_HEIGHT = 425
	OBSTACLE_MIN_WIDTH = 150
	OBSTACLE_MAX_WIDTH = 425

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
		self.screenbuf = Surface((self.BUF_WIDTH, self.BUF_HEIGHT))
		self.velocity = self.GAME_VELOCITY
		self.screenbuf_delta_x = 0

		self.player = Character();
		self.clock  = pygame.time.Clock();

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

	def update(self):
		if (self.player.state == self.player.CHARACTER_STATE_ALIVE):
			self.screenbuf_delta_x -= self.velocity
			if (self.screenbuf_delta_x < -self.GAME_WIDTH):

				# Screenbuf depleted. Copy second half of screenbuf to first,
				# generate new second half, set buf -> screen blit delta to 0

				sbuf = self.screenbuf

				sbuf.fill(Colors.BLACK, Rect(0, 0, self.GAME_WIDTH, self.GAME_HEIGHT))
				sbuf.blit(sbuf, (0, 0), Rect(self.GAME_WIDTH, 0, self.GAME_WIDTH, self.GAME_HEIGHT));

				sbuf.fill(Colors.BLACK, Rect(self.GAME_WIDTH, 0, self.GAME_WIDTH, self.GAME_HEIGHT))
				self.generateObstacles(self.GAME_WIDTH)

				self.screenbuf_delta_x = 0

		self.player.update();
		if (self.player.checkCollision(self.obstacles) == True):
			self.player.startAnimationDeath();

	def draw(self):
		self.player.draw(self.screenbuf);
		self.screen.blit(self.screenbuf, (self.screenbuf_delta_x, 0));

	def getVelocity(self):
		return self.velocity

	def generateObstacles(self, startx=200):
		self.obstacles = pygame.sprite.Group();
		w = max(self.OBSTACLE_MIN_WIDTH, int(random() * self.OBSTACLE_MAX_WIDTH))
		h = max(self.OBSTACLE_MIN_HEIGHT, int(random() * self.OBSTACLE_MAX_HEIGHT))

		x = startx
		maxx = self.screenbuf.get_rect().right

		while (x < maxx):
			xdelta = int(random() * 1200)
			xdelta = min(700, xdelta)
			x += xdelta

			w = max(self.OBSTACLE_MIN_WIDTH, int(random() * self.OBSTACLE_MAX_WIDTH))
			h = max(self.OBSTACLE_MIN_HEIGHT, int(random() * self.OBSTACLE_MAX_HEIGHT))

			if (x + w > maxx): # break if wall goes over buffer edge
				break

			obstacle = Obstacle(w, h)
			obstacle.draw(self.screenbuf, x)
			self.obstacles.add(obstacle)

			x += w
