import pygame
import items.crossitem as crossitem
import math
import random

class MagicWeapon(crossitem.CrossItem):
    def __init__(self, game, path = "assets/sprites/magic_weapon.png"):
        self.scale = 200
        self.rot_angle = 35
        self.offsetx = 100
        self.offsety = -75
        super().__init__(game, path)
        self.timer_speed = 100
        self.accuracy = 0.01
        self.range = 100

        self.mana_cost = 10

        #damage is calculated by projectile damage

    def check_useable(self):
        if self.timer_done == True:
            self.useable = True
            self.timer_done = False
        else:
            self.useable = False

    def use(self):
        if self.useable == True and self.game.player.entity.mana > 0:
            a = self.game.player.angle
            accuracy_offset = random.uniform(-self.accuracy, self.accuracy)
            self.game.player.entity.mana -= self.mana_cost
            self.game.projectile_handler.fire(pygame.math.Vector2(self.game.player.x, self.game.player.y), pygame.math.Vector2(math.cos(self.game.player.angle+accuracy_offset), math.sin(self.game.player.angle+accuracy_offset)))