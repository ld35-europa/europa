import pygame

class MusicPlayer:

	def __init__(self, character):
		self.speed = 0.005
		self.character = character
		pygame.mixer.init(44100, -16, 2, 32768)
		self.music_fire = pygame.mixer.Sound("assets/sounds/music_fire.ogg")
		self.music_water = pygame.mixer.Sound("assets/sounds/music_water.ogg")
		#TODO: get the initial desired sound from the character.
		self.fire_vol = 1
		self.water_vol = 0
		self.fire_desired_vol = 1
		self.water_desired_vol = 0
		if not pygame.mixer.Channel(1).get_busy():
			pygame.mixer.Channel(1).play(self.music_fire, -1)
		if not pygame.mixer.Channel(2).get_busy():
			pygame.mixer.Channel(2).play(self.music_water, -1)
		self.music_fire.set_volume(self.fire_vol)
		self.music_water.set_volume(self.water_vol)

	def update(self):
		if self.character.type == self.character.CHARACTER_TYPE_FIRE:
			self.fire_desired_vol = 1
			self.water_desired_vol = 0
		else:
			self.fire_desired_vol = 0
			self.water_desired_vol = 1
		if self.fire_desired_vol == 1 and self.fire_vol <= 1:
			self.fire_vol +=self.speed
			if self.water_vol > 0 + self.speed:
				self.water_vol -=self.speed
			if self.water_vol < 0:
				self.water_vol = 0
			if self.water_vol < self.speed and self.water_desired_vol == 0:
				self.water_vol = 0

		if self.water_desired_vol == 1 and self.water_vol <= 1:
			self.water_vol += self.speed
			if self.fire_vol > 0 + self.speed:
				self.fire_vol -= self.speed
			if self.fire_vol < 0:
				self.fire_vol = 0
			if self.fire_vol < self.speed and self.fire_desired_vol == 0:
				self.fire_vol = 0
		self.music_fire.set_volume(self.fire_vol)
		self.music_water.set_volume(self.water_vol)
