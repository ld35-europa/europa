#!/usr/bin/env python2

import pygame

class Character:

	jump_start_position_x = 0;
	jump_start_position_y = 0;

	CHARACTER_IMAGES = ["assets/img/char.png"];
	CHARACTER_FISH = CHARACTER_IMAGES[0];

	JUMP_LENGTH = 200
	JUMP_HEIGTH_MULT = 2.5

	MODE_JUMP = 1;
	MODE_IDLE = 0;

	mode = MODE_IDLE;

	def __init__(self, character_type, screen):
		self.screen = screen
		self.character_image = pygame.image.load(character_type)
		self.character_rect = self.character_image.get_rect()
		self.character_rect.bottom = 300

	def startJump(self):
		self.jump_start_position_x = self.character_rect.left
		self.jump_start_position_y = self.character_rect.bottom
		self.mode = self.MODE_JUMP;

	def jump(self):
		half_jump_length = self.JUMP_LENGTH / 2.0
		jump_height = self.JUMP_LENGTH / 2.0 * self.JUMP_HEIGTH_MULT

		x = self.character_rect.left
		y = self.character_rect.bottom

		xdelta = x - self.jump_start_position_x + 8
		xpara = (xdelta - half_jump_length) / half_jump_length
		ypara = xpara ** 2
		ydelta = jump_height - (ypara * jump_height)

		self.character_rect.left = self.jump_start_position_x + xdelta
		self.character_rect.bottom = self.jump_start_position_y - ydelta

		if (xdelta >= self.JUMP_LENGTH):
			self.character_rect.bottom = self.jump_start_position_y
			return False
		return True

	def move(self):
		if (self.mode == self.MODE_JUMP):
			if (self.jump() == False):
				self.mode = self.MODE_IDLE;

		self.screen.blit(self.character_image, self.character_rect)