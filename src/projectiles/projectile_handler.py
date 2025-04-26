import pygame
from settings import *
import sprites.sprite as sprite
import projectiles.projectile as projectile
import json

class ProjectileHandler:
    def __init__(self, game):
        self.game = game
        self.sprites = []

    def fire(self, start_dir, end_dir, range):
        self.sprites.append(projectile.ProjectileObject(self.game, range, dir = end_dir, pos = (start_dir.x, start_dir.y)))

    def update(self):
        for i, sprite in enumerate(self.sprites):
            print(sprite.norm_dist)
            if sprite.update():
                self.sprites.pop(i)
            if sprite.check_wall():
                self.sprites.pop(i)
            if sprite.norm_dist > sprite.range:
                self.sprites.pop(i)
        
    def clear_all(self):
        self.sprites = []