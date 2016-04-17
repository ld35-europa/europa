#!/usr/bin/env python2

import math
import pygame

from pygame import Rect
from pygame import Surface
from lib.Colors import Colors
from lib.CachedAsset import load_cached_asset

class Fluid(pygame.sprite.Sprite):
	FLUID_TYPE_WATER = 1
	FLUID_TYPE_LAVA = 2

	def __init__(self, ftype, rect):
		super(Fluid, self).__init__();
		self.ftype = ftype
		self.rect = rect

		if (ftype == self.FLUID_TYPE_LAVA):
			self.image = load_cached_asset("assets/img/fluid/lava.png")
		else:
			self.image = load_cached_asset("assets/img/fluid/water.png")

	def draw(self, surface, dstrect):

		# Blit filling the destination rect horizontally

		srcrect = self.image.get_rect()
		blit_right_x = 0
		
		while (blit_right_x < dstrect.right):
			surface.blit(self.image, (dstrect.left + blit_right_x, dstrect.top))
			blit_right_x += srcrect.width

	def getType(self):
		return self.ftype

	def getColor(self):
		color = None

		if (self.ftype == self.FLUID_TYPE_LAVA):
			color = Colors.RED
		else:
			color = Colors.BLUE
		return color
