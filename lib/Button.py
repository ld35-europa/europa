import pygame
from pygame import Rect
from pygame import Surface


class Button:
    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, x, y, width, height, imagePath):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = Rect(x, y, width, height)
        self.image = pygame.image.load(imagePath)

    def render(self, screen):
        screen.blit(self.image, self.rect)
