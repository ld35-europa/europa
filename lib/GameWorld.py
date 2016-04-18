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

	SCENE_BUF_WIDTH = GAME_WIDTH*2
	SCENE_BUF_HEIGHT = GAME_HEIGHT
	GAME_FPS = 120;
	ANIMATION_FPS = GAME_FPS / 3;
	ACCELERATION = 0.05

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
	
	DEBUG_NOCOLL_OBSTACLES = False
	DEBUG_RECT_OBSTACLES = False
	DEBUG_RECT_FLUIDS = False

	state = STATE_MENU

	BACKGROUND_COLOR = Colors.BLACK;

	def __init__(self, menu):
		pygame.init()
		pygame.display.set_caption('Europa')

		self.menu = menu
		self.screen = pygame.display.set_mode(self.GAME_DIMENSION);
		self.scenebuf = Surface((self.SCENE_BUF_WIDTH, self.SCENE_BUF_HEIGHT))
		self.backbuf = Surface((self.GAME_WIDTH, self.GAME_HEIGHT))

		self.velocity = 0
		self.scenebuf_delta_x = 0 # x delta to backbuffer

		self.player = Character()
		self.obstacles = pygame.sprite.Group()
		self.fluids = pygame.sprite.Group()
		self.first_fluid = None
		self.last_fluid = None

		self.music_player = MusicPlayer(self.player)
		self.clock  = pygame.time.Clock();
		self.game_start_t = 0
		self.destroyed = False

		# Initial backgrounds

		bg_dest_rect = self.screen.get_rect()
		self.fillBackground(self.scenebuf, bg_dest_rect)
		bg_dest_rect.left += self.GAME_WIDTH
		self.fillBackground(self.scenebuf, bg_dest_rect)

	def start(self):
		self.generateScene()
		self.initPlayer()
		self.updateVelocity(True)

		while (not self.destroyed):
			self.clock.tick(self.GAME_FPS)

			for e in pygame.event.get():
				if (e.type == pygame.QUIT):
					self.state = self.STATE_FINISHED
					sys.exit(0);
				elif (e.type == pygame.KEYDOWN):
					if (self.player.state == self.player.CHARACTER_STATE_ALIVE):
						if e.key == pygame.K_q:
							self.player.transform()
						elif e.key == pygame.K_SPACE:
							self.player.startJump()
						elif (e.key == pygame.K_LEFT):
							self.player.inputx -= 1
						elif (e.key == pygame.K_RIGHT):
							self.player.inputx += 1
					if (e.key == pygame.K_ESCAPE):
						sys.exit(0)
					if (e.key == pygame.K_RETURN and \
						(self.state == self.STATE_MENU or self.state == self.STATE_FINISHED) \
					):
						self.menu.createNew(self)
				elif (e.type == pygame.KEYUP):
					if e.key == pygame.K_SPACE:
						self.player.jumping = False
					elif (e.key == pygame.K_LEFT):
						self.player.inputx += 1
					elif (e.key == pygame.K_RIGHT):
						self.player.inputx -= 1
				elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
					if self.state == self.STATE_MENU or self.state == self.STATE_FINISHED:
						self.menu.checkClick(pygame.mouse.get_pos(), self)

			if (self.state == self.STATE_PLAYING):
				self.update();
				self.draw();
				pygame.display.flip()
			elif (self.state == self.STATE_MENU or self.state == self.STATE_FINISHED):
				self.menu.render(self)

	def update(self):
		if (self.player.state == self.player.CHARACTER_STATE_ALIVE):
			self.scenebuf_delta_x -= self.velocity
			
			if (self.scenebuf_delta_x < -self.GAME_WIDTH):
				self.resetSceneBuffer()
				
		elif (\
			self.player.animation == self.player.ANIMATION_NONE and \
			self.player.state == self.player.CHARACTER_STATE_DEAD\
		):
			self.state = self.STATE_FINISHED
		
		self.updateVelocity()
		self.music_player.update()
		self.player.update()
		
		obstacleCollisionSprite = self.player.checkCollision(self.obstacles, self.scenebuf_delta_x)
		if (obstacleCollisionSprite != False):
			self.obstacles.remove(obstacleCollisionSprite)
			self.player.startAnimationDeath();

		fluidCollisionSprite = \
			self.player.checkCollision(self.fluids, self.scenebuf_delta_x);
			
		if (fluidCollisionSprite != False):
			if (\
				fluidCollisionSprite.ftype == Fluid.FLUID_TYPE_LAVA and \
				self.player.type == self.player.CHARACTER_TYPE_WATER \
			):
				self.fluids.remove(fluidCollisionSprite)
				self.player.startAnimationDeath();
			elif (\
				fluidCollisionSprite.ftype == Fluid.FLUID_TYPE_WATER and \
				self.player.type == self.player.CHARACTER_TYPE_FIRE \
			):
				self.fluids.remove(fluidCollisionSprite)
				self.player.startAnimationDeath();

	def draw(self):

		# scenebuf -> backbuf -> screen
		
		self.backbuf.blit(self.scenebuf, (self.scenebuf_delta_x, 0));
		self.drawBackbufDebug()
		self.player.draw(self.backbuf);
		self.screen.blit(self.backbuf, (0, 0))

	def drawBackbufDebug(self):
		
		# Helper function to draw debug rectangles. If color is a
		# callable, receives a sprite as the argument and is expected
		# to return a color
		
		def drawDebugRects(sgroup, color_cb):
			for s in (sgroup):
				color = color_cb(s)
								
				srect = Rect(s.rect)
				srect.left += self.scenebuf_delta_x
				srect.top = self.GAME_HEIGHT - 50
				self.backbuf.fill(color, srect)
		
		def getObstacleColor(s):
			return Colors.GREEN
			
		def getFluidColor(s):
			if (s.getType() == Fluid.FLUID_TYPE_LAVA):
				return Colors.RED
			return Colors.BLUE
		
		if (self.obstacles and self.DEBUG_RECT_OBSTACLES):
			drawDebugRects(self.obstacles, getObstacleColor)
		if (self.fluids and self.DEBUG_RECT_FLUIDS):
			drawDebugRects(self.fluids, getFluidColor)

	def getVelocity(self):
		return self.velocity

	def resetSceneBuffer(self):
		
		# Screenbuf depleted. Copy second half of scenebuf to first,
		# generate new second half, set buf -> screen blit delta to 0

		sbuf = self.scenebuf

		self.fillBackground(sbuf, Rect(0, 0, self.GAME_WIDTH, self.GAME_HEIGHT))
		sbuf.blit(sbuf, (0, 0), Rect(self.GAME_WIDTH, 0, self.GAME_WIDTH, self.GAME_HEIGHT));

		self.fillBackground(sbuf, Rect(self.GAME_WIDTH, 0, self.GAME_WIDTH, self.GAME_HEIGHT))
		self.updateSpriteRects(self.obstacles)
		self.updateSpriteRects(self.fluids)
		self.generateScene(self.GAME_WIDTH)

		self.scenebuf_delta_x = 0

	def fillBackground(self, dst_surface, dst_rect):

		# dst_rect represents both the destination on dst_surface and
		# the size of the background image portion. The background is
		# expected to be mirrored on the y-axis: the horizontal center
		# portion is blitted to surface.

		bg = load_cached_asset("assets/img/background.png")
		bgrect = bg.get_rect()
		bgsrcx = int((bgrect.width / 2.0) - (dst_rect.width / 2.0))

		dst_surface.blit(bg, dst_rect, Rect(bgsrcx, 0, dst_rect.width, dst_rect.height))

	def initPlayer(self):

		# Set player initial phase

		ftype = self.first_fluid.getType()
		self.player.type = \
			Character.CHARACTER_TYPE_FIRE \
			if ftype == Fluid.FLUID_TYPE_LAVA \
			else Character.CHARACTER_TYPE_WATER

	def updateVelocity(self, reset=False):
		if (reset):
			self.game_start_t = pygame.time.get_ticks()

		t = pygame.time.get_ticks()
		dt = t - self.game_start_t
		self.velocity = ((dt / 1000.0) * self.ACCELERATION) + 1

	def destroy(self):
		self.destroyed = True

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

			if (not self.first_fluid):
				self.first_fluid = f
			self.last_fluid = f
			self.fluids.add(f)
			f.draw(self.scenebuf, r)

	def generateObstacles(self, rects):
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
	
	def updateSpriteRects(self, spritegroup):
		
		# Update sprite rectangles at new scene portion generation. The new
		# portion of the scene is generated to the second half of the scenebuf
		# (W=GAME_WIDTH*2), while all old sprites are blitted to the first half of
		# the scenebuf. Hence, subtract GAME_WIDTH from the rect x of each. Also
		# clean up old sprites far off the left of the scene.
		
		for s in (spritegroup):
			s.rect.left -= self.GAME_WIDTH
			if (s.rect.right < -self.GAME_WIDTH):
				spritegroup.remove(s)
