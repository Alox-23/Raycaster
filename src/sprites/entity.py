import sprites.sprite as sprite
import pygame
from settings import *

class Entity(sprite.SpriteObject):
    def __init__(self, game, pos = (0, 0), path = "assets/sprites/goblin/wall.png", scale = 1, shift = 0):
        super().__init__(game, path, pos = pos, scale = scale, shift = shift)
        self.health = 100