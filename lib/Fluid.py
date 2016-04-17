#!/usr/bin/env python2

import math
import pygame

from pygame import Rect
from pygame import Surface
from lib.Colors import Colors

class Fluid:
	FLUID_TYPE_WATER = 1
	FLUID_TYPE_LAVA = 2

	def __init__(self, ftype, rect):
		self.ftype = ftype
		self.rect = rect

	def get(self):
		pass

	def getType(self):
		return self.ftype

	def getColor(self):
		color = None

		if (self.ftype == self.FLUID_TYPE_LAVA):
			color = Colors.RED
		else:
			color = Colors.BLUE
		return color
