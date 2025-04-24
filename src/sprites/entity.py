import sprites.sprite as sprite
import pygame
from settings import *

class Entity(sprite.SpriteObject):
    def __init__(self, game, pos = (0, 0), path = "assets/sprites/goblin/wall.png", scale = 1, shift = 0, p = None):
        super().__init__(game, path, pos = pos, scale = scale, shift = shift, p = p)
        self.killable = True

        self.health = 50
        self.max_health = 100
        self.mana = 50
        self.max_mana = 100
        self.stamina = 50
        self.max_stamina = 100

        self.health_regen = 0.003
        self.mana_regen = 0.01
        self.stamina_regen = 0.02

    def regen_mana(self):
        if self.mana < self.max_mana:
            self.mana += self.mana_regen * self.game.delta_time
        else:
            self.mana = self.max_mana
    def regen_health(self):
        if self.health < self.max_health:
            self.health += self.health_regen * self.game.delta_time
        else:
            self.health = self.max_health
    def regen_stamina(self):
        if self.stamina < self.max_stamina:
            self.stamina += self.stamina_regen * self.game.delta_time
        else:
            self.stamina = self.max_stamina

    def regen_all(self):
        self.regen_health()
        self.regen_mana()
        self.regen_stamina()

    def update(self):
        super().update()
        self.regen_all()