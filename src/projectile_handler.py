import pygame
from settings import *
import sprite
import projectile
import json

class ProjectileHandler:
    def __init__(self, game):
        self.game = game
        self.sprites = []

    def fire(self, start_dir, end_dir):
        self.sprites.append(projectile.ProjectileObject(self.game, dir = end_dir, pos = (start_dir.x+end_dir.x, start_dir.y+end_dir.y)))

    def update(self):
        for i, sprite in enumerate(self.sprites):
            sprite.update()
            if sprite.check_wall():
                self.sprites.pop(i)
            if sprite.draw_image.get_width() < 3:
                print("lol")
                self.sprites.pop(i)
        
    def clear_all(self):
        self.sprites = []