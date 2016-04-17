#!/usr/bin/env python2

import pygame
import sys
import time
import random

from pygame import Surface
from pygame import Rect

import lib.Colors
from lib.Character import Character
from lib.Colors import Colors
from lib.Obstacle import Obstacle
from lib.Fluid import Fluid
from lib.MusicPlayer import MusicPlayer
from lib.CachedAsset import load_cached_asset

class GameWorld:
	GAME_WIDTH = 1280
	GAME_HEIGHT = 800
	GAME_DIMENSION = [GAME_WIDTH, GAME_HEIGHT]
	GAME_VELOCITY_X = 1;

	BUF_WIDTH = GAME_WIDTH*2
	BUF_HEIGHT = GAME_HEIGHT
	GAME_FPS = 120;
	ANIMATION_FPS = GAME_FPS / 3;

	FLUID_MIN_W = 400
	FLUID_MAX_W = 1000

	OBSTACLE_MIN_HEIGHT = 125
	OBSTACLE_MAX_HEIGHT = 125
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
		self.velocity = self.GAME_VELOCITY_X
		self.screenbuf_delta_x = 0

		self.player = Character()
		self.music_player = MusicPlayer(self.player)
		self.obstacles = None
		self.fluids = None
		self.last_fluid = None

		self.clock  = pygame.time.Clock();

	def start(self):
		self.generateScene();
		self.state = self.STATE_PLAYING;

		while self.state != self.STATE_FINISHED:
			self.clock.tick(self.GAME_FPS);

			for e in pygame.event.get():
				if (e.type == pygame.QUIT):
					self.state = self.STATE_FINISHED
					sys.exit(0);
				elif (e.type == pygame.KEYDOWN):
					if (self.player.state == self.player.CHARACTER_STATE_ALIVE):
						if (e.key == pygame.K_2):
							self.player.startAnimationTransform(self.player.ANIMATION_TRANSFORM_TO_FIRE)
						if (e.key == pygame.K_3):
							self.player.startAnimationTransform(self.player.ANIMATION_TRANSFORM_TO_WATER)
						if e.key == pygame.K_SPACE:
							self.player.startJump()
						if (e.key == pygame.K_LEFT):
							self.player.inputx -= 1
						if (e.key == pygame.K_RIGHT):
							self.player.inputx += 1
					if (e.key == pygame.K_ESCAPE):
						sys.exit(0)

				elif (e.type == pygame.KEYUP):
					if e.key == pygame.K_SPACE:
						self.player.jumping = False
					if (e.key == pygame.K_LEFT):
						self.player.inputx += 1
					if (e.key == pygame.K_RIGHT):
						self.player.inputx -= 1

			self.update();
			self.draw();
			self.music_player.update()

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
				self.generateScene(self.GAME_WIDTH)

				self.screenbuf_delta_x = 0

		self.player.update();
		if (self.player.checkCollision(self.obstacles) != False):
			self.player.startAnimationDeath();

		if (self.fluids != None):
			fluidCollisionSprite = self.player.checkCollision(self.fluids);
			if (fluidCollisionSprite != False):
				if (fluidCollisionSprite.ftype == Fluid.FLUID_TYPE_LAVA and self.player.type == self.player.CHARACTER_TYPE_WATER):
					self.player.startAnimationDeath();
				elif (fluidCollisionSprite.ftype == Fluid.FLUID_TYPE_WATER and self.player.type == self.player.CHARACTER_TYPE_FIRE):
					self.player.startAnimationDeath();

	def draw(self):
		self.player.draw(self.screenbuf);
		self.screen.blit(self.screenbuf, (self.screenbuf_delta_x, 0));

	def getVelocity(self):
		return self.velocity

	def generateScene(self, startx=0):

		# Generate a new scene into the screen buffer, starting from x
		# position startx

		x = startx
		maxx = self.BUF_WIDTH
		fluid_rects = []

		# Generate fluid rects

		while (x < maxx):
			w = random.randrange(self.FLUID_MIN_W, self.FLUID_MAX_W+1)
			h = load_cached_asset("assets/img/fluid/lava.png").get_rect().height
			print h;
			# If the next rect were smaller than FLUID_MIN_W, stretch
			# current to scene end. If the current rect is past scene end,
			# chop off excess.

			if ((maxx - (x + w) < self.FLUID_MIN_W) or (x + w > maxx)):
				w = maxx - x

			r = Rect(x, self.GAME_HEIGHT-h+50, w, h)
			fluid_rects.append(r)
			x += w

		# Generate fluid pools and obstacles based on fluid rects

		self.generateFluid(fluid_rects)
		self.generateObstacles(fluid_rects)

	def generateFluid(self, rects):

		# Generate fluid pools (Fluid class) according to the
		# passed Rect list

		self.fluids = pygame.sprite.Group();

		for r in (rects):
			f = None

			# If first fluid pool in scene, it must be of the same type as
			# last fluid pool in the last scene. Random otherwise.

			if (r == rects[0] and self.last_fluid):
				f = Fluid(self.last_fluid.getType(), r)
			else:
				if (int(random.random() * 2)):
					f = Fluid(Fluid.FLUID_TYPE_LAVA, r)
				else:
					f = Fluid(Fluid.FLUID_TYPE_WATER, r)

			self.last_fluid = f
			self.fluids.add(f)
			f.draw(self.screenbuf, r)

	def generateObstacles(self, rects):

		# Generate obstacles between the passed rects

		self.obstacles = pygame.sprite.Group();

		for r in rects:
			if (r == rects[-1]):
				break

			xcenter = r.right
			w = random.randrange(self.OBSTACLE_MIN_WIDTH, self.OBSTACLE_MAX_WIDTH+1)
			h = random.randrange(self.OBSTACLE_MIN_HEIGHT, self.OBSTACLE_MAX_HEIGHT+1)
			x = int(xcenter - (w/2.0))

			obstacle = Obstacle(w, h)
			obstacle.draw(self.screenbuf, x)
			self.obstacles.add(obstacle)
