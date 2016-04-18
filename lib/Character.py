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
	ANIMATION_JUMP = 4;
	ANIMATION_NONE = 5;

	FRAMES_SWIM = 7;
	FRAMES_DEATH_FIRE = 7;
	FRAME_DEATH_WATER = 9;
	FRAMES_TRANSFORM = 9;
	FRAMES_JUMP = 3;

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
		self.createCharater();
		self.rect.bottom = self.GameWorld.GAME_HEIGHT
		self.last_time = pygame.time.get_ticks();

		self.starting_y = (2.0/3.0) * self.GameWorld.GAME_HEIGHT;

		self.vx = 0
		self.vy = 0

		self.px = 100
		self.py = self.starting_y

		self.inputx = 0 # -1 = left, 1 = right
		self.jumping = False
		self.jumpcapacity = 1

		self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.ogg")
		self.shapeshift_sound = pygame.mixer.Sound("assets/sounds/shapeshift.ogg")
		self.death_sound = pygame.mixer.Sound("assets/sounds/sizzle.ogg")

	def startAnimationSwim(self):
		self.animation = self.ANIMATION_SWIM
		self.frame = 0

	def startAnimationDeath(self):
		#pygame.mixer.find_channel().play(self.death_sound) # doesn't work for me
		self.animation = self.ANIMATION_DEATH
		self.frame = 0
		self.state = self.CHARACTER_STATE_DEAD

	def startAnimationTransform(self, animation):
		if (animation == self.ANIMATION_TRANSFORM_TO_FIRE and self.type == self.CHARACTER_TYPE_WATER):
			pygame.mixer.find_channel().play(self.shapeshift_sound)
			self.frame = self.FRAMES_TRANSFORM
			self.type = self.CHARACTER_TYPE_FIRE
			self.animation = self.ANIMATION_TRANSFORM_TO_FIRE
		elif (animation == self.ANIMATION_TRANSFORM_TO_WATER and self.type == self.CHARACTER_TYPE_FIRE):
			pygame.mixer.find_channel().play(self.shapeshift_sound)
			self.type = self.CHARACTER_TYPE_WATER
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

	def animationJump(self):
		if (self.vy < 0):
			if (self.frame + 1 <= self.FRAMES_JUMP):
				self.frame += 1;
			else:
				self.frame = 0;
		else:
			self.startAnimationSwim()
		self.createCharater();

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
		elif (self.animation == self.ANIMATION_JUMP):
			image_path = "assets/img/" + self.type + "/jump/" + str(self.frame) + ".png";
		else:
			image_path = "assets/img/" + self.type + "/" + self.state + "/" + str(self.frame) + ".png";

		self.image = pygame.image.load(image_path);
		if (hasattr(self, 'rect')):
			rect = self.image.get_rect()
			rect.height = rect.height / 2;
			rect.left = self.rect.left
			rect.bottom = self.rect.bottom
			self.rect = rect
		else:
			self.rect = self.image.get_rect()
			self.rect.height = self.rect.height / 2

	def update(self):
		time_between = pygame.time.get_ticks() - self.last_time;

		if (self.state == self.CHARACTER_STATE_ALIVE):
			## jumping logic
			if self.jumping:
				self.vy += -4.0 * self.jumpcapacity
				self.jumpcapacity *= 0.9

			inwater = self.py > self.starting_y
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
				if (self.animation == self.ANIMATION_JUMP):
					self.animationJump()
			 	elif (self.animation == self.ANIMATION_SWIM):
					self.animationSwim();
				elif (self.animation == self.ANIMATION_TRANSFORM_TO_FIRE or self.animation == self.ANIMATION_TRANSFORM_TO_WATER):
					self.animationTransform();

	def draw(self, surface):
		surface.blit(self.image, self.rect)

	def checkCollision(self, sprite_group, surfaces_delta_x):
		def collision_detector(sprite1, sprite2):
			collrect = Rect(sprite2.rect)

			# Some grace distance on left / right for Obstacle

			if (type(sprite2) is lib.Obstacle.Obstacle):
				coll_grace = collrect.width / 3
				collrect.left += surfaces_delta_x
				collrect.left += coll_grace
				collrect.width -= (coll_grace * 2)

			return sprite1.rect.colliderect(collrect)

		for sprite in pygame.sprite.spritecollide(self, sprite_group, 0, collision_detector):
			return sprite
		return False;

	def startJump(self):
		self.jumping = True
		if (self.type == self.CHARACTER_TYPE_WATER):
			self.animation = self.ANIMATION_JUMP;
			self.frame = 0;
		pygame.mixer.find_channel().play(self.jump_sound)
