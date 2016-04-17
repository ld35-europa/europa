
import pygame
import sys
from pygame import sprite
from pygame import image
from lib.GameWorld import GameWorld
from lib.Button import Button
from lib.Colors import Colors
from lib.GameWorld import GameWorld
from lib.Character import Character

class Menu:

	def __init__(self):

		x = GameWorld.GAME_DIMENSION[0]/2
		y = GameWorld.GAME_DIMENSION[1]/2
		self.startButton = Button(x, y, "assets/img/menu/start.png")

		x = GameWorld.GAME_DIMENSION[0]/1.7
		y = GameWorld.GAME_DIMENSION[1]/1.222
		self.againButton = Button(x, y, "assets/img/menu/again.png")

		self.background = image.load("assets/img/menu/start_background.png")
		self.background_rect = self.background.get_rect()
		self.gameover = image.load("assets/img/menu/gameover.png")
		self.gameover_rect = self.gameover.get_rect()


	def render(self, game):
		self.game = game
		self.game.screen.fill(Colors.BLACK)

		if self.game.state == self.game.STATE_MENU:
			self.game.screen.blit(self.background, self.background_rect)
			self.startButton.render(self.game.screen)
		else:
			self.game.screen.blit(self.gameover, self.gameover_rect)
			self.againButton.render(self.game.screen)
		pygame.display.flip()

	def checkClick(self, mouse, game):
		if game.state == game.STATE_MENU and self.startButton.rect.collidepoint(mouse[0], mouse[1]):
			game.state = game.STATE_PLAYING

		elif game.state == game.STATE_FINISHED and self.againButton.rect.collidepoint(mouse[0], mouse[1]):
			game.state = game.STATE_PLAYING
			self.game.player = Character()
			self.game.generateScene();
			self.game.screenbuf_delta_x = 0