import pygame
from crossitem import CrossItem

class MeleWeapon(CrossItem):
    def __init__(self, game, path):
        super().__init__(game, path)
        self.damage = 10
        self.timer_speed = 1

    def use(self):
        if self.useable == True:
            self.col_sprite[1].health -= self.damage