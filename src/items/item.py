import pygame
from settings import *
from items.crosshair import *

class Item:
    def __init__(self, game, path):
        self.game = game

        self.swing_index = -0.5
        self.swing_bool = False
        self.swing_amplitude = 50
        self.swing_speed = 0.01

        self.in_range = True
        self.timer_done = False
        self.timer_speed = 300
        self.timer = 0
        self.useable = False

        try:
            self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(path), (self.scale, self.scale)), self.rot_angle).convert_alpha()
        except:
            self.scale = 600
            self.rot_angle = 35
            self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(path), (self.scale, self.scale)), self.rot_angle).convert_alpha()

        self.image.set_colorkey((0,0,0))
        
        self.rect = self.image.get_rect()

        try:
            self.calculate_rect()
        except:
            self.offsetx = -200
            self.offsety = -200
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
            pygame.draw.line(d, (0, 255, 0), (0, self.rect.centery), (WIDTH, self.rect.centery), 5)
            pygame.draw.line(d, (0, 0, 255), (self.rect.centerx, 0), (self.rect.centerx, HEIGHT), 5)

    def update(self):
        self.check_timer()
        self.check_useable()
        self.swing_animation()

    def use(self):
        if self.useable == True:
            print("im being used!") 

    def check_useable(self):
        if self.in_range == True and self.timer_done == True:
            self.useable = True
            self.timer_done = False
        else:
            self.useable = False

    def check_timer(self):
        if self.timer < self.timer_speed:
            self.timer += 1 * self.game.delta_time
        else:
            self.timer_done = True
            self.timer = 0
    
    def swing_animation(self):
        self.swing_speed = self.game.player.speed / 5
        x = 0
        y = 0

        if (self.game.player.dx != 0 or self.game.player.dy != 0) or (self.game.player.dx != 0 and self.game.player.dy != 0):
            self.calculate_rect()
        else:
            if self.swing_index > -0.4 or self.swing_index < -0.6:
                self.calculate_rect()
            