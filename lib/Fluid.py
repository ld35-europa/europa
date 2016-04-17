#!/usr/bin/env python2

import math
import pygame

from pygame import Rect
from pygame import Surface
from lib.Colors import Colors
from lib.CachedAsset import load_cached_asset

class Fluid(pygame.sprite.Sprite):
	FLUID_TYPE_WATER = "water"
	FLUID_TYPE_LAVA = "lava"

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
		blit_delta_x = 0

		while ((dstrect.left + blit_delta_x) < dstrect.right):
			dstx = dstrect.left + blit_delta_x
			blitarea = None

			if (dstx + srcrect.width > dstrect.right):
				blitarea = Rect(0, 0, dstrect.right-dstx, srcrect.height)

			surface.blit(self.image, (dstx, dstrect.top), blitarea)
			blit_delta_x += srcrect.width

	def update(self):
		return True;

	def getType(self):
		return self.ftype

	def getColor(self):
		color = None

		if (self.ftype == self.FLUID_TYPE_LAVA):
			color = Colors.RED
		else:
			color = Colors.BLUE
		return color
