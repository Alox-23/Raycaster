import pygame
from settings import *
import sprite
import json

class SpriteHandler:
    def __init__(self, game):
        self.game = game
        self.sprites = []

    def load_sprites(self, data):
        self.sprites = []

        for s in data["sprites"]:
            self.sprites.append(sprite.SpriteObject(self.game, pos = (s[1][0], s[1][1])))

    def update(self):
        for sprite in self.sprites:
            sprite.update()