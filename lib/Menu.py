
import pygame
import sys

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
		x = dimensions[0]/2 - self.buttonWidth/2
		y = dimensions[1]/3 - self.buttonHeight/2

		self.startButton = Button(x, y, self.buttonWidth, self.buttonHeight, "assets/img/menu/start_button.png")
		y = y + self.buttonHeight + self.padding

		self.optionsButton = Button(x, y, self.buttonWidth, self.buttonHeight, "assets/img/menu/options_button.png")
		y = y + self.buttonHeight + self.padding

		self.exitButton = Button(x, y, self.buttonWidth, self.buttonHeight, "assets/img/menu/exit_button.png")

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

		self.exitButton.render(self.screen)
		self.startButton.render(self.screen)
		self.optionsButton.render(self.screen)

		if self.mouseDown:
			if self.exitButton.rect.collidepoint(mouseX, mouseY):
				print("davai exitButton hit and shit")

				sys.exit(52)
			if self.startButton.rect.collidepoint(mouseX, mouseY):
				print("davai startButton hit and shit")

				self.screen.fill((Colors.BLACK))
				self.game.state = self.game.STATE_PLAYING
				self.game.start()

		pygame.display.flip()