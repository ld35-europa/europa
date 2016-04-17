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

	ACTION_JUMP = 0
	ACTION_IDLE = 2;

	JUMP_LENGTH = 200
	JUMP_HEIGHT_MULT = 2.5

	ANIMATION_SWIM = 0;
	ANIMATION_DEATH = 1;
	ANIMATION_TRANSFORM_TO_FIRE = 2;
	ANIMATION_TRANSFORM_TO_WATER = 3;
	ANIMATION_NONE = 4;

	FRAMES_SWIM = 7;
	FRAMES_DEATH = 7;
	FRAMES_TRANSFORM = 9;

	action = ACTION_IDLE
	animation = ANIMATION_SWIM
	type = CHARACTER_TYPE_FIRE
	state = CHARACTER_STATE_ALIVE

	frame = 0

	def __init__(\
		self, character_type = CHARACTER_TYPE_FIRE, character_state = CHARACTER_STATE_ALIVE, \
		frame_num = 0 \
	):
		super(Character, self).__init__();
		self.type = character_type
		self.state = character_state
		self.frame = frame_num
		self.GameWorld = lib.GameWorld.GameWorld
		self.last_rect = Rect(0, 0, 0, 0)
		self.createCharater();
		self.rect.bottom = self.GameWorld.GAME_HEIGHT
		self.last_time = pygame.time.get_ticks();


	def startAnimationSwim(self):
		self.animation = self.ANIMATION_SWIM
		self.frame = 0

	def startAnimationDeath(self):
		self.animation = self.ANIMATION_DEATH
		self.frame = 0
		self.state = self.CHARACTER_STATE_DEAD

	def startAnimationTransform(self, animation):
		if (animation == self.ANIMATION_TRANSFORM_TO_FIRE and self.type == self.CHARACTER_TYPE_WATER):
			self.frame = self.FRAMES_TRANSFORM
			self.animation = self.ANIMATION_TRANSFORM_TO_FIRE
		elif (animation == self.ANIMATION_TRANSFORM_TO_WATER and self.type == self.CHARACTER_TYPE_FIRE):
			self.frame = 0
			self.animation = self.ANIMATION_TRANSFORM_TO_WATER

	def animationDeath(self):
		if (self.frame + 1 <= self.FRAMES_DEATH):
			self.frame += 1;
			self.createCharater();
		else:
			self.animation = self.ANIMATION_NONE;

	def animationSwim(self):
		if (self.frame + 1 <= self.FRAMES_SWIM):
			self.frame += 1;
		else:
			self.startAnimationSwim()
		self.createCharater();

	def animationTransform(self):
		if (self.animation == self.ANIMATION_TRANSFORM_TO_FIRE):
			if (self.frame - 1 >= 0):
				self.frame -= 1;
				self.createCharater();
			else:
				self.type = self.CHARACTER_TYPE_FIRE;
				self.startAnimationSwim();
		elif (self.animation == self.ANIMATION_TRANSFORM_TO_WATER):
			if (self.frame + 1 <= self.FRAMES_TRANSFORM):
				self.frame += 1;
				self.createCharater();
			else:
				self.type = self.CHARACTER_TYPE_WATER;
				self.startAnimationSwim()

	def createCharater(self):
		if (self.animation == self.ANIMATION_TRANSFORM_TO_FIRE or self.animation == self.ANIMATION_TRANSFORM_TO_WATER):
			image_path = "assets/img/transform/" + str(self.frame) + ".png";
		else:
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
		self.action = self.ACTION_JUMP;

	def actionJump(self):
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
		time_between = pygame.time.get_ticks() - self.last_time;

		if (self.action == self.ACTION_JUMP):
			if (self.actionJump() == False):
				self.action = self.ACTION_IDLE;

		if (time_between >= self.GameWorld.ANIMATION_FPS and self.animation != self.ANIMATION_NONE):
			self.last_time = pygame.time.get_ticks();

			if (self.animation == self.ANIMATION_DEATH):
				self.animationDeath();

			if (self.state == self.CHARACTER_STATE_ALIVE):
			 	if (self.animation == self.ANIMATION_SWIM):
					self.animationSwim();
				elif (self.animation == self.ANIMATION_TRANSFORM_TO_FIRE or self.animation == self.ANIMATION_TRANSFORM_TO_WATER):
					self.animationTransform();


	def draw(self, surface):
		surface.fill(Colors.BLACK, self.last_rect)
		surface.blit(self.image, self.rect)
		self.last_rect = Rect(self.rect)

	def checkCollision(self, sprite_group):
		for sprite in pygame.sprite.spritecollide(self, sprite_group, 1):
			return True
		return False;


