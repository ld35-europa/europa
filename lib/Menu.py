
import pygame
import sys
from pygame import sprite
from pygame import image
from lib.GameWorld import GameWorld
from lib.Button import Button
from lib.Colors import Colors


class Menu:

	buttonWidth = 300
	buttonHeight = 150
	padding = 10
	mouseDown = False

	def __init__(self, dimensions):
		pygame.init()
		pygame.display.set_caption('Europa')
		self.game = GameWorld()
		self.game.state = self.game.STATE_MENU

		self.screen = pygame.display.set_mode(dimensions)
		x = dimensions[0]/2
		y = dimensions[1]/2

		self.startButton = Button(x, y, "assets/img/menu/start.png")
		self.background = image.load("assets/img/menu/start_background.png")
		self.background_rect = self.background.get_rect()


	def start(self):
		while self.game.state == self.game.STATE_MENU:
			self.render()

	def render(self):
		self.screen.fill((Colors.BLACK))
		self.mouseDown = False
		mouseX, mouseY = pygame.mouse.get_pos()

		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				sys.exit(44)
			if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
				self.mouseDown = True
			if (e.type == pygame.KEYDOWN):
				if e.key == pygame.K_RETURN:
					self.game.state = self.game.STATE_PLAYING
					self.game.start()
		if self.mouseDown:
			if self.startButton.rect.collidepoint(mouseX, mouseY):
				self.game.state = self.game.STATE_PLAYING
				self.game.start()
		self.screen.blit(self.background, self.background_rect)
		self.startButton.render(self.screen)
		pygame.display.flip()
