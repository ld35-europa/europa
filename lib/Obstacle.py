#!/usr/bin/env python2

import math
import pygame
from random import random

import pygame.sprite
from pygame import Rect
from pygame import Surface

import lib.GameWorld
from lib.Colors import Colors
from lib.CachedAsset import load_cached_asset

# Class reprenting an obstacle between the fluid pools

class Obstacle(pygame.sprite.Sprite):

	Y_VARIABILITY = 10
	Y_BIAS_MULT = 1.8

	def __init__(self, width, height):
		super(Obstacle, self).__init__()
		self.obstacletxt = load_cached_asset("assets/img/obstacle4.png")
		self.create(width, height),

	def create(self, width, height):

		# Sculpt a obstacle into a surface (width w, height w), initially
		# a solid block, by subtracting from each pixel column, in the
		# left hand side and right hand side of the rect separately.
		# YVAR is the maximum variability from a straight diagonal
		# line (to either side), Y_BIAS_MULT determines how flat-
		# topped the obstacles are. Returns the surface.

		sfc = Surface((width, height))
		self.rect = sfc.get_rect();
		self.rect.bottom = lib.GameWorld.GameWorld.GAME_HEIGHT

		lhs, rhs = self.splitRectVertically(Rect(0, 0, width, height))
		drop_per_x = float(rhs.height) / rhs.width

		YVAR = 10
		Y_BIAS_MULT = 2.0

		sfc.blit(self.obstacletxt, (0, 0))
		sfc.set_colorkey(Colors.GREEN)

		# Generate obstacle

		for side in (lhs, rhs):
			last_y = -1
			startx = side.left
			i_mult = 1

			if (side == lhs):
				startx = side.right-1
				i_mult = -1

			for i in xrange(side.width):
				x = startx+(i*i_mult)
				y = side.top + i*drop_per_x

				reverse_progress = ((1.0 - float(i) / side.width) * 100 + 1)
				reverse_progress_log = math.log(reverse_progress, 100)
				ybias = -reverse_progress_log * YVAR * Y_BIAS_MULT
				yjitter = (YVAR - random()*YVAR*2 + ybias)
				y = round(y + yjitter)

				if (y < last_y):
					y = last_y
				last_y = y

				sfc.fill(Colors.GREEN, Rect(x, side.top, 1, y-side.top))

		self.image = sfc;

	def splitRectVertically(self, rect):
		lhs = Rect(rect.left, rect.top, rect.centerx-rect.left, rect.height)
		rhs = Rect(rect.centerx, rect.top, rect.right-rect.centerx, rect.height)
		return (lhs, rhs)

	def draw(self, surface, x):
		self.rect.left = x
		surface.blit(self.image, self.rect)
