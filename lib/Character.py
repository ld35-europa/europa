#!/usr/bin/env python2

import pygame
import lib.GameWorld

from lib.Colors import Colors
from pygame import Rect

class Character:

	jump_start_position_x = 0;
	jump_start_position_y = 0;

	CHARACTER_IMAGES = ["assets/img/char.png"];
	CHARACTER_FISH = CHARACTER_IMAGES[0];

	JUMP_LENGTH = 200
	JUMP_HEIGHT_MULT = 2.5

	MODE_JUMP = 1;
	MODE_IDLE = 0;

	mode = MODE_IDLE;

	def __init__(self, character_type, screen):
		self.GameWorld = lib.GameWorld.GameWorld
		self.screen = screen
		self.image = pygame.image.load(character_type)
		self.rect = self.image.get_rect()
		self.last_rect = Rect(0, 0, 0, 0)
		self.rect.bottom = self.GameWorld.GAME_HEIGHT

	def startJump(self):
		self.jump_start_position_x = self.rect.left
		self.jump_start_position_y = self.rect.bottom
		self.mode = self.MODE_JUMP;

	def jump(self):
		half_jump_length = self.JUMP_LENGTH / 2.0
		jump_height = self.JUMP_LENGTH / 2.0 * self.JUMP_HEIGHT_MULT

		x = self.rect.left
		y = self.rect.bottom

		xdelta = x - self.jump_start_position_x + 8
		xpara = (xdelta - half_jump_length) / half_jump_length
		ypara = xpara ** 2
		ydelta = jump_height - (ypara * jump_height)

		self.rect.left = self.jump_start_position_x + xdelta
		self.rect.bottom = self.jump_start_position_y - ydelta

		if (xdelta >= self.JUMP_LENGTH):
			self.rect.bottom = self.jump_start_position_y
			return False
		return True

	def move(self):
		if (self.mode == self.MODE_JUMP):
			if (self.jump() == False):
				self.mode = self.MODE_IDLE;

		self.screen.fill(Colors.BLACK, self.last_rect)
		self.screen.blit(self.image, self.rect)
		self.last_rect = Rect(self.rect)

