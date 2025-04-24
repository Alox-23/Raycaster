import pygame
from settings import *

class CrossHair():
    def __init__(self, game, width = 5):
        self.game = game
        self.image = pygame.Surface((width, 5))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (HALF_WIDTH, HALF_HEIGHT)

    def set_color(self, c):
        self.image.fill(c)

    def draw(self, d):
        d.blit(self.image, self.rect)