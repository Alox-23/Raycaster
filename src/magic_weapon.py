import pygame
import crossitem

class MagicWeapon(crossitem.CrossItem):
    def __init__(self, game, path = "assets/sprites/magic_weapon.png"):
        super().__init__(game, path)
        self.timer_speed = 1
        self.range = 100

        self.damage = 10

    def use(self):
        if self.useable == True:
            try:
                self.col_sprite[1].health -= self.damage
            except:
                pass