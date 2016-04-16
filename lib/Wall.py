#!/usr/bin/env python2

from pygame import Rect
from lib.Colors import Colors
from random import random
import math


# Sculpt a wall within the passed rect by subtracting from
# each pixel column, in the left hand side and right hand side
# of the rect separately. YVAR is the maximum variability from
# a straight diagonal line (to either side), Y_BIAS_MULT determines
# how flat-topped the obstacles are.

class Wall:

	YVAR = 10
	Y_BIAS_MULT = 1.8

	def __init__(self, left, top, width, height):
		self.wall_rect = Rect(left, top, width, height);

	def drawOnScreen(self, screen):
		lhs, rhs = self.splitRectangleVertically(self.wall_rect)
		drop = float(rhs.height) / rhs.width

		screen.fill(Colors.RED, self.wall_rect)

		for side in (lhs, rhs):
			last_y = -1
			startx = side.left
			i_mult = 1

			if (side == lhs):
				startx = side.right-1
				i_mult = -1

			for i in xrange(side.width):
				x = startx+(i*i_mult)
				y = side.top + i*drop

				prog = ((1.0 - float(i) / side.width) * 100 + 1)
				prog_log = math.log(prog, 100)
				ybias = -prog_log * self.YVAR * self.Y_BIAS_MULT
				yjitter = (self.YVAR - random() * self.YVAR * 2 + ybias)
				y = round(y + yjitter)

				if (y < last_y):
					y = last_y
				last_y = y

				screen.fill(Colors.BLACK, Rect(x, side.top, 1, y-side.top))

	def splitRectangleVertically(self, rect):
		lhs = Rect(rect.left, rect.top, rect.centerx-rect.left, rect.height)
		rhs = Rect(rect.centerx, rect.top, rect.right-rect.centerx, rect.height)
		return (lhs, rhs)