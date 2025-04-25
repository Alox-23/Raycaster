import pygame
import sys
import time
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprites.sprite import *
from sprites.sprite_handler import *
from projectiles.projectile_handler import *
from hud import *
from items.crosshair import *

class GAME:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("assets/fonts/font.ttf", 16)
        self.debug_text = ""
        self.display = pygame.display.set_mode(RES, flags = D_FLAGS)
        self.resize_buffer = pygame.Surface(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.togle_text = False
        self.new_game()

    def new_game(self):
        self.sprite_handler = SpriteHandler(self)
        self.projectile_handler = ProjectileHandler(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.player = PLAYER(self)
        self.hud = Hud(self)
        self.map = Map(self)

    def load_resize_buffer(self):
        self.object_renderer.load_resize_buffer()

    def update(self):
        self.debug_text = ""
        self.hud.update()
        rstart = time.time()
        self.raycasting.update()
        rend = time.time()
        self.debug_text += f"Raycasting time: {rend-rstart :.3f};"
        pstart = time.time()
        self.player.update()
        pend = time.time()
        self.debug_text += f"Player time: {pend-pstart :.5f};"
        sstart = time.time()
        self.sprite_handler.update()
        self.projectile_handler.update()
        send = time.time()
        self.debug_text += f"Sprite time: {send-sstart :.5f};"
        self.delta_time = self.clock.tick(FPS)
        
    def update_text(self):
        self.debug_text += f'FPS: {self.clock.get_fps() :.1f}' + ";"
        self.debug_text += ";"
        self.debug_text += "Player pos: " + str(int(self.player.x)) + ", " + str(int(self.player.y)) + ";"
        self.debug_text += "Player Angle: " + str(round(math.degrees(self.player.angle), 0)) + ";"
        self.debug_text += ";"
        self.debug_text += "Projectiles: " + str(len(self.projectile_handler.sprites)) + ";"

    def draw(self):
        dstart = time.time()
        self.object_renderer.draw()
        dend = time.time()
        self.debug_text += f"Draw time: {dend-dstart :.3f};"

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and self.togle_text == False:
                    self.togle_text = True
                elif event.key == pygame.K_p and self.togle_text == True:
                    self.togle_text = False
        return True

    def run(self):
        while True:
            if not self.check_events():
                break
            self.update()
            self.draw()
            self.update_text()
            if self.togle_text:
                self.object_renderer.draw_text()
                pygame.display.update()


if __name__ == '__main__':
    game = GAME()
    game.run()
    pygame.quit()
    sys.exit()
