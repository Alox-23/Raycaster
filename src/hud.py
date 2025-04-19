import pygame
from settings import *

class Bar:
    def __init__(self, pos, m_val= 100, val = 50, height = 20, scale = 2, border_size = 3):
        self.max_val = m_val
        self.val = val
        self.scale = scale
        self.height = height

        self.border_size = border_size

        self.image = pygame.Surface((self.max_val * self.scale + self.border_size*2, self.height + self.border_size*2))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.bg_color = (100, 100, 100)
        self.border_color = (1,1,1)
        self.color = (255, 0, 0)

    def draw(self, display):
        display.blit(self.image, self.rect)

    def update(self, val):
        if val > self.max_val:
            self.val = self.max_val
        else:
            self.val = val
        self.image.fill(self.border_color)
        pygame.draw.rect(self.image, self.bg_color, pygame.Rect((self.border_size, self.border_size), (self.max_val*self.scale, self.height)))
        pygame.draw.rect(self.image, self.color, pygame.Rect((self.border_size, self.border_size), (self.val*self.scale, self.height)))

class CenterBar(Bar):
    def update(self, val):
        if val > self.max_val:
            self.val = self.max_val
        else:
            self.val = val
        self.image.fill(self.border_color)
        pygame.draw.rect(self.image, self.bg_color, pygame.Rect((self.border_size, self.border_size), (self.max_val*self.scale, self.height)))
        pygame.draw.rect(self.image, self.color, pygame.Rect(((self.max_val*self.scale-self.val*self.scale)/2+self.border_size, self.border_size), (self.val*self.scale, self.height)))

class RightBar(Bar):
    def update(self, val):
        if val > self.max_val:
            self.val = self.max_val
        else:
            self.val = val
        self.image.fill(self.border_color)
        pygame.draw.rect(self.image, self.bg_color, pygame.Rect((self.border_size, self.border_size), (self.max_val*self.scale, self.height)))
        pygame.draw.rect(self.image, self.color, pygame.Rect(((self.max_val - self.val)*2+self.border_size, self.border_size), (self.val*self.scale, self.height)))

class Hud:
    def __init__(self, game):
        self.game = game

        self.hud_height = 100
        self.image = pygame.Surface((WIDTH, self.hud_height))
        self.image.set_colorkey((0,5,0))

        self.rect = self.image.get_rect()
        self.rect.topleft = (0, HEIGHT - self.hud_height)

        self.mana = Bar((8, self.hud_height-25), height=15, border_size = 2)
        self.stamina = Bar((8, self.hud_height-45), height=15 , border_size = 2)
        self.health = Bar((8, self.hud_height-65), height=15 , border_size = 2)

        self.game.player.player_hands_rect.center = (HALF_WIDTH, self.hud_height-50)

        self.mana.color = (0, 0, 255)
        self.health.color = (255, 0, 0)
        self.stamina.color = (0, 255, 0)

    def draw(self, display):
        self.image.fill((0,5,0))
        self.game.player.draw_hands(self.image)
        self.health.draw(self.image)
        self.mana.draw(self.image)
        self.stamina.draw(self.image)
        display.blit(self.image, self.rect)

    def update(self):
        self.health.update(self.game.player.health)
        self.mana.update(self.game.player.mana)
        self.stamina.update(self.game.player.stamina)

        self.health.max_val = self.game.player.max_health
        self.mana.max_val = self.game.player.max_mana
        self.stamina.max_val = self.game.player.max_stamina