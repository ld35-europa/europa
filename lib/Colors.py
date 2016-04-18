#!/usr/bin/env python2

import pygame
from random import random

class Colors:
	RED = pygame.Color(255, 0, 0)
	GREEN = pygame.Color(0, 255, 0)
	BLUE = pygame.Color(0, 0, 255)
	BLACK = pygame.Color(0, 0, 0)

def getRandColor():
	return (int(random()*256), int(random()*256), int(random()*256))
