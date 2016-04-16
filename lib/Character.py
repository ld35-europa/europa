#!/usr/bin/env python2

import pygame

class Character:

	position_x = 0;
	position_y = 0;

	CHARACTER_IMAGES = ["assets/img/char.png"];
	CHARACTER_FISH = CHARACTER_IMAGES[0];

	JUMP_LENGTH = 200
	JUMP_HEIGTH_MULT = 2.5


	def __init__(self, character_type):
		self.character_image = pygame.image.load(character_type)
		self.character_rect = self.character_image.get_rect()
		self.character_rect.bottom = 300

	def jump(self):
		self.position_x = self.character_rect.left
		self.position_y = self.character_rect.bottom

		half_jump_length = self.JUMP_LENGTH / 2.0
		jump_height = self.JUMP_LENGTH / 2.0 * self.JUMP_HEIGTH_MULT

		x = self.character_rect.left
		y = self.character_rect.bottom

		xdelta = x - self.position_x + 8
		xpara = (xdelta - half_jump_length) / half_jump_length
		ypara = xpara ** 2
		ydelta = jump_height - (ypara * jump_height)

		self.character_rect.left = self.position_x + xdelta
		self.character_rect.bottom = self.position_y - ydelta

		if (xdelta >= self.JUMP_LENGTH):
			self.character_rect.bottom = self.position_y
			return False
		return True