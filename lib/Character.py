#!/usr/bin/env python2

import pygame
import lib.GameWorld
import pygame.sprite
import time

from lib.Colors import Colors
from pygame import Rect

class Character(pygame.sprite.Sprite):

	CHARACTER_TYPE_FIRE = 'fire';
	CHARACTER_TYPE_WATER = 'water';

	CHARACTER_STATE_ALIVE = 'alive';
	CHARACTER_STATE_DEAD = 'dead';

	ANIMATION_SWIM = 0;
	ANIMATION_DEATH = 1;
	ANIMATION_TRANSFORM_TO_FIRE = 2;
	ANIMATION_TRANSFORM_TO_WATER = 3;
	ANIMATION_NONE = 4;

	FRAMES_SWIM = 7;
	FRAMES_DEATH_FIRE = 7;
	FRAME_DEATH_WATER = 9;
	FRAMES_TRANSFORM = 9;

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

		self.vx = 0
		self.vy = 0

		self.px = 100
		self.py = (2.0/3.0) * self.GameWorld.GAME_HEIGHT

		self.inputx = 0 # -1 = left, 1 = right
		self.jumping = False
		self.jumpcapacity = 1


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
		if (self.type == self.CHARACTER_TYPE_WATER):
			death_frames = self.FRAME_DEATH_WATER;
		else:
			death_frames = self.FRAMES_DEATH_FIRE;

		if (self.frame + 1 <= death_frames):
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

	def update(self):
		time_between = pygame.time.get_ticks() - self.last_time;

		if (self.state == self.CHARACTER_STATE_ALIVE):
			## jumping logic
			if self.jumping:
				self.vy += -4.0 * self.jumpcapacity
				self.jumpcapacity *= 0.9

			inwater = self.py > (2.0/3.0) * self.GameWorld.GAME_HEIGHT
			if inwater:
				if self.vy > 0:
					self.vy *= 0.7
					if not self.jumping:
						self.jumpcapacity = 1
			else:
				self.vy += 1.0

			## left/right logic
			if self.inputx != 0:
				movement_velocity = 5
				self.vx = self.inputx * movement_velocity
			else:
				self.vx = 0;

			## physics update
			self.px = self.px + self.vx # * dt
			self.py = self.py + self.vy # * dt

			self.rect.left = self.px - self.rect.width / 2
			self.rect.top = self.py - self.rect.height / 2

		##animations
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
		surface.blit(self.image, self.rect)
		self.last_rect = Rect(self.rect)

	def checkCollision(self, sprite_group):
		for sprite in pygame.sprite.spritecollide(self, sprite_group, 1):
			return True
		return False;
