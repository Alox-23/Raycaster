import pygame
from settings import *

class Item:
    def __init__(self, game, path):
        self.game = game

        self.swing_index = -0.51
        self.swing_bool = False
        self.swing_amplitude = 100
        self.swing_speed = self.game.player.speed / 5

        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(path), (600, 600)), 35)
        self.offsetx = -150
        self.offsety = -200
        self.rect = self.image.get_rect()

        self.calculate_rect()
    
    def calculate_rect(self):
        
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

    def draw(self, d):
        d.blit(self.image, self.rect)

        if self.game.togle_text == True:
            pygame.draw.line(d, (255, 0, 0), (0, self.rect.centery), (WIDTH, self.rect.centery), 5)
            pygame.draw.line(d, (0, 0, 255), (self.rect.centerx, 0), (self.rect.centerx, HEIGHT), 5)

    def update(self):
        self.swing_animation()
    
    def swing_animation(self):
        print(self.swing_index)
        x = 0
        y = 0

        if (self.game.player.dx != 0 or self.game.player.dy != 0) or (self.game.player.dx != 0 and self.game.player.dy != 0):
            self.calculate_rect()
        else:
            if self.swing_index > -0.5 or self.swing_index < -0.52:
                self.calculate_rect()