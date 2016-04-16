#!/usr/bin/env python2

import sys
import pygame
import time
import math

from random import random
from pygame import Rect
from pygame import Surface

JUMPLEN = 200
JUMPH_MULT = 2.5
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 255)

def main():
	pygame.init()
	size = w, h = 640, 480

	screen = pygame.display.set_mode(size)

	char = pygame.image.load("assets/img/char.png")
	charrect = char.get_rect()
	last_charrect = Rect(0, 0, 0, 0)

	jumpmode = False
	jumpstartx = 0
	jumpstarty = 0

	charrect.bottom=h

	wall = sculpt_obstacle(150, 300)
	screen.blit(wall, (450, h-300))
	wall = sculpt_obstacle(225, 200)
	screen.blit(wall, (150, h-200))

	while 1:
		for e in pygame.event.get():
			if (e.type == pygame.QUIT):
				sys.exit(0);
			elif (e.type == pygame.KEYDOWN):
				if (e.key == 32):
					jumpmode = True
					jumpstartx = charrect.left
					jumpstarty = charrect.bottom
				elif (e.key == 27):
					sys.exit(0)
				else:
					print e

		if (jumpmode):
			jumpmode = jump(charrect, jumpstartx, jumpstarty)

		#if (charrect.left < 0 or charrect.right > w):
		#	speed[0] = -speed[0]
		#if (charrect.top < 0 or charrect.bottom > h):
		#	speed[1] = -speed[1]

		screen.fill(BLACK, last_charrect)
		screen.blit(char, charrect)
		last_charrect = Rect(charrect)
		pygame.display.flip()
		time.sleep(1.0/30)

def sculpt_obstacle(w, h):

	# Sculpt a wall into a surface (width w, height w), initially
	# a solid block, by subtracting from each pixel column, in the
	# left hand side and right hand side of the rect separately.
	# YVAR is the maximum variability from a straight diagonal
	# line (to either side), Y_BIAS_MULT determines how flat-
	# topped the obstacles are. Returns the surface.

	sfc = Surface((w, h))
	lhs, rhs = split_rect_vert(Rect(0, 0, w, h))
	drop_per_x = float(rhs.height) / rhs.width
	walltxt = pygame.image.load("assets/img/wall2.png")

	YVAR = 10
	Y_BIAS_MULT = 2.0

	sfc.blit(walltxt, (0, 0))

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

			prog = ((1.0 - float(i) / side.width) * 100 + 1)
			prog_log = math.log(prog, 100)
			ybias = -prog_log * YVAR * Y_BIAS_MULT
			yjitter = (YVAR - random()*YVAR*2 + ybias)
			y = round(y + yjitter)

			if (y < last_y):
				y = last_y
			last_y = y

			sfc.fill(TRANSPARENT, Rect(x, side.top, 1, y-side.top))

	return sfc

def split_rect_vert(rect):
	lhs = Rect(rect.left, rect.top, rect.centerx-rect.left, rect.height)
	rhs = Rect(rect.centerx, rect.top, rect.right-rect.centerx, rect.height)
	return (lhs, rhs)

def jump(rect, startx, starty):

	# Jump routine. Takes a rect and starting coordinates as
	# arguments. Returns true if jump sequence has ended, false
	# otherwise.

	halfjl=JUMPLEN/2.0
	jumph = JUMPLEN/2.0*JUMPH_MULT

	x = rect.left
	y = rect.bottom
	xdelta = x-startx+8
	xpara = (xdelta - halfjl) / halfjl
	ypara = xpara**2
	ydelta = jumph-(ypara*jumph)

	rect.left = startx + xdelta
	rect.bottom = starty - ydelta

	if (xdelta >= JUMPLEN):
		rect.bottom = starty
		return False
	return True

main()

