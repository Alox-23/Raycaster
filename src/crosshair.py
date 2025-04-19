import pygame
from settings import *

class CrossHair():
    def __init__(self, game):
        self.game = game
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (HALF_WIDTH, HALF_HEIGHT)

    def draw(self, d):
        d.blit(self.image, self.rect)