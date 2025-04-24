import pygame
from items.crossitem import CrossItem

class MeleWeapon(CrossItem):
    def __init__(self, game, path):
        super().__init__(game, path)
        self.damage = 10
        self.timer_speed = 300

        self.stamina_cost = 10

    def use(self):
        if self.useable == True and self.game.player.stamina > 0:
            try:
                self.col_sprite[1].health -= self.damage
                self.game.player.stamina -= self.stamina_cost
            except:
                pass