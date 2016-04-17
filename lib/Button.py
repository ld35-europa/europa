import pygame
from pygame import Rect
from pygame import Surface


class Button:
    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, x, y, imagePath):
        self.x = x
        self.y = y
        self.image = pygame.image.load(imagePath)
        self.tmp_rect = self.image.get_rect()
        self.rect = Rect(x-self.tmp_rect[2]/2, y-self.tmp_rect[3]/2, self.tmp_rect[2], self.tmp_rect[3])

    def render(self, screen):
        screen.blit(self.image, self.rect)
