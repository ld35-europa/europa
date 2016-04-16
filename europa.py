#!/usr/bin/env python2

import sys
import pygame
import time

JUMPLEN = 200

def main():
	pygame.init()
	size = w, h = 640, 480
	black = 0, 0, 0
	
	screen = pygame.display.set_mode(size)
	char = pygame.image.load("assets/img/char.png")
	charrect = char.get_rect()
	jumpmode = False
	jumpstartx = 0
	jumpstarty = 0
	
	charrect.bottom=h
	
	while 1:
		for e in pygame.event.get():
			if (e.type == pygame.QUIT):
				sys.exit(0);
			elif (e.type == pygame.KEYDOWN):
				if (e.key == 32):
					jumpmode = True
					jumpstartx = charrect.left
					jumpstarty = charrect.bottom
		
		if (jumpmode):
			jumpmode = jump(charrect, jumpstartx, jumpstarty)
		
		#if (charrect.left < 0 or charrect.right > w):
		#	speed[0] = -speed[0]
		#if (charrect.top < 0 or charrect.bottom > h):
		#	speed[1] = -speed[1]
		
		screen.fill(black)
		screen.blit(char, charrect)
		pygame.display.flip()
		time.sleep(1.0/30)

def jump(rect, startx, starty):
	
	# Jump routine. Takes a rect and starting coordinates as
	# arguments. Returns true if jump sequence has ended, false
	# otherwise.
	
	jumph = JUMPLEN/2.0
	
	x = rect.left
	y = rect.bottom
	xdelta = x-startx+5
	xpara = (xdelta - jumph) / jumph
	ypara = xpara**2
	ydelta = jumph-(ypara*jumph)
	
	rect.left = startx + xdelta
	rect.bottom = starty - ydelta
	
	if (xdelta >= JUMPLEN):
		rect.bottom = starty
		return False
	return True

main()

