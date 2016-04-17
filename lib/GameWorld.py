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

	SCENE_BUF_WIDTH = GAME_WIDTH*2
	SCENE_BUF_HEIGHT = GAME_HEIGHT
	GAME_FPS = 120;
	ANIMATION_FPS = GAME_FPS / 3;

	FLUID_MIN_W = 400
	FLUID_MAX_W = 1000

	OBSTACLE_MIN_HEIGHT = 200
	OBSTACLE_MAX_HEIGHT = 325
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
		self.scenebuf = Surface((self.SCENE_BUF_WIDTH, self.SCENE_BUF_HEIGHT))
		self.backbuf = Surface((self.GAME_WIDTH, self.GAME_HEIGHT))

		self.velocity = self.GAME_VELOCITY_X
		self.scenebuf_delta_x = 0

		self.player = Character()
		self.obstacles = None
		self.fluids = None
		self.last_fluid = None

		self.music_player = MusicPlayer(self.player)
		self.clock  = pygame.time.Clock();

		# Initial backgrounds

		bg_dest_rect = self.screen.get_rect()
		self.fillBackground(self.scenebuf, bg_dest_rect)
		bg_dest_rect.left += self.GAME_WIDTH
		self.fillBackground(self.scenebuf, bg_dest_rect)

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
			self.scenebuf_delta_x -= self.velocity
			if (self.scenebuf_delta_x < -self.GAME_WIDTH):

				# Screenbuf depleted. Copy second half of scenebuf to first,
				# generate new second half, set buf -> screen blit delta to 0

				sbuf = self.scenebuf

				self.fillBackground(sbuf, Rect(0, 0, self.GAME_WIDTH, self.GAME_HEIGHT))
				sbuf.blit(sbuf, (0, 0), Rect(self.GAME_WIDTH, 0, self.GAME_WIDTH, self.GAME_HEIGHT));

				self.fillBackground(sbuf, Rect(self.GAME_WIDTH, 0, self.GAME_WIDTH, self.GAME_HEIGHT))
				self.generateScene(self.GAME_WIDTH)

				self.scenebuf_delta_x = 0

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

		# scenebuf -> backbuf -> screen

		self.backbuf.blit(self.scenebuf, (self.scenebuf_delta_x, 0));
		self.player.draw(self.backbuf);
		self.screen.blit(self.backbuf, (0, 0))

	def getVelocity(self):
		return self.velocity

	def fillBackground(self, dst_surface, dst_rect):

		# dst_rect represents both the destination on dst_surface and
		# the size of the background image portion. The background is
		# expected to be mirrored on the y-axis: the horizontal center
		# portion is blitted to surface.

		bg = load_cached_asset("assets/img/background.png")
		bgrect = bg.get_rect()
		bgsrcx = int((bgrect.width / 2.0) - (dst_rect.width / 2.0))

		dst_surface.blit(bg, dst_rect, Rect(bgsrcx, 0, dst_rect.width, dst_rect.height))

	def generateScene(self, startx=0):

		# Generate a new scene into the screen buffer, starting from x
		# position startx

		x = startx
		maxx = self.SCENE_BUF_WIDTH
		fluid_rects = []

		# Generate fluid rects

		while (x < maxx):
			w = random.randrange(self.FLUID_MIN_W, self.FLUID_MAX_W+1)
			h = load_cached_asset("assets/img/fluid/lava.png").get_rect().height

			# If the next rect were smaller than FLUID_MIN_W, stretch
			# current to scene end. If the current rect is past scene end,
			# chop off excess.

			if ((maxx - (x + w) < self.FLUID_MIN_W) or (x + w > maxx)):
				w = maxx - x

			r = Rect(x, self.GAME_HEIGHT-h, w, h)
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
			f.draw(self.scenebuf, r)

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
			obstacle.draw(self.scenebuf, x)
			self.obstacles.add(obstacle)
