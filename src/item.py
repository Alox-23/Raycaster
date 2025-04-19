import pygame
from settings import *

class Item:
    def __init__(self, game, path):
        self.game = game

        self.swing_index = -1
        self.swing_bool = False
        self.swing_amplitude = 100
        self.swing_speed = self.game.player.speed / 5

        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(path), (600, 600)), 35)
        self.offsetx = -50
        self.offsety = -200
        self.rect = self.image.get_rect()
        self.rect.topleft = ((HALF_WIDTH+self.offsetx, HUD_HEIGHT-self.image.get_height()-self.offsety))
        

    def draw(self, d):
        d.blit(self.image, self.rect)

    def update(self):
        self.swing_animation()
    
    def swing_animation(self):
        x = 0
        y = 0

        if (self.game.player.dx != 0 or self.game.player.dy != 0) or (self.game.player.dx != 0 and self.game.player.dy != 0):
            if self.swing_bool is False:
                self.swing_index += self.swing_speed * self.game.delta_time
            else:
                self.swing_index -= self.swing_speed * self.game.delta_time

            if self.swing_index < -1:
                self.swing_bool = False
            if self.swing_index > 0:
                self.swing_bool = True

            x = -math.cos(self.swing_index*math.pi)
            y = -math.sin(self.swing_index*math.pi)/2

            self.rect.x = x * self.swing_amplitude + HALF_WIDTH+self.offsetx
            self.rect.y = y * self.swing_amplitude + HUD_HEIGHT-self.image.get_height()-self.offsety