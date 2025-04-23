import pygame
from settings import *
import entity
import json

class SpriteHandler:
    def __init__(self, game):
        self.game = game
        self.sprites = []

    def load_sprites(self, data):
        self.sprites = []

        for s in data["sprites"]:
            self.sprites.append([0, entity.Entity(self.game, pos = (s[1][0], s[1][1]))])
            self.sprites[-1][1].update()
            self.sprites[-1][0] = self.sprites[-1][1].rect

    def update(self):
        for sprite in self.sprites:
            sprite[1].update()
            sprite[0] = sprite[1].rect
            if sprite[1].health <= 0:
                self.sprites.remove(sprite)
