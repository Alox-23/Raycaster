import pygame
from settings import *
import sprites.sprite as sprite
import projectiles.projectile as projectile
import json

class ProjectileHandler:
    def __init__(self, game):
        self.game = game
        self.sprites = []

    def fire(self, start_dir, end_dir):
        self.sprites.append(projectile.ProjectileObject(self.game, dir = end_dir, pos = (start_dir.x, start_dir.y)))

    def update(self):
        for i, sprite in enumerate(self.sprites):
            if sprite.update():
                self.sprites.pop(i)
            if sprite.check_wall():
                self.sprites.pop(i)
            if sprite.norm_dist > 200:
                self.sprites.pop(i)
        
    def clear_all(self):
        self.sprites = []