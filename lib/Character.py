#!/usr/bin/env python2

import pygame
import lib.GameWorld
import pygame.sprite
import time

from lib.Colors import Colors
from pygame import Rect

class Character(pygame.sprite.Sprite):

	jump_start_position_x = 0;
	jump_start_position_y = 0;

	CHARACTER_TYPE_FIRE = 'fire';
	CHARACTER_TYPE_WATER = 'water';
	CHARACTER_STATE_ALIVE = 'alive';
	CHARACTER_STATE_DEAD = 'dead';

	JUMP_LENGTH = 200
	JUMP_HEIGHT_MULT = 2.5

	MODE_JUMP = 0
	MODE_DOUBLE_JUMP = 1
	MODE_IDLE = 2;
	MODE_DIE = 3;

	TOTAL_FRAMES = 7;

	mode = MODE_IDLE;
	type = CHARACTER_TYPE_FIRE
	state = CHARACTER_STATE_ALIVE
	frame = 0

	def __init__(self, character_type = CHARACTER_TYPE_FIRE, character_state = CHARACTER_STATE_ALIVE, frame_num = 0):
		super(Character, self).__init__();
		self.type = character_type
		self.state = character_state
		self.frame = frame_num
		self.GameWorld = lib.GameWorld.GameWorld
		self.last_rect = Rect(0, 0, 0, 0)
		self.createCharater();
		self.rect.bottom = self.GameWorld.GAME_HEIGHT


	def startDie(self):
		self.mode = self.MODE_DIE
		self.frame = 0
		self.state = self.CHARACTER_STATE_DEAD


	def die(self):
		time.sleep(1.0 / 10)
		if (self.frame + 1 <= self.TOTAL_FRAMES):
			self.frame += 1;
			self.createCharater();


	def createCharater(self):
		image_path = "assets/img/" + self.type + "/" + self.state + "/" + str(self.frame) + ".png";
		self.image = pygame.image.load(image_path);
		if (hasattr(self, 'rect')):
			rect = self.image.get_rect()
			rect.left = self.rect.left
			rect.bottom = self.rect.bottom
			self.rect = rect
		else:
			self.rect = self.image.get_rect()

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

	def update(self):
		if (self.mode == self.MODE_JUMP):
			if (self.jump() == False):
				self.mode = self.MODE_IDLE;

		if (self.mode == self.MODE_DIE):
			if (self.die() == False):
				self.mode = self.MODE_IDLE;

	def draw(self, surface):
		surface.fill(Colors.BLACK, self.last_rect)
		surface.blit(self.image, self.rect)
		self.last_rect = Rect(self.rect)

