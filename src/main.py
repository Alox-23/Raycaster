import pygame
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite import *
from sprite_handler import *
from projectile_handler import *
from hud import *

class GAME:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("assets/fonts/font.ttf", 16)
        self.debug_text = ""
        self.display = pygame.display.set_mode(RES)
        self.resize_buffer = pygame.Surface(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.togle_text = True
        self.new_game()

    def new_game(self):
        self.hud = Hud(self)
        self.projectile_handler = ProjectileHandler(self)
        self.player = PLAYER(self)
        self.sprite_handler = SpriteHandler(self)
        self.object_renderer = ObjectRenderer(self)
        self.map = Map(self)
        self.raycasting = RayCasting(self)

    def load_resize_buffer(self):
        self.object_renderer.load_resize_buffer()

    def update(self):
        self.debug_text = ""
        self.hud.update()
        self.player.update()
        self.raycasting.update()
        self.sprite_handler.update()
        self.projectile_handler.update()
        self.delta_time = self.clock.tick(FPS)
        self.update_text()
        
    def update_text(self):
        self.debug_text += f'FPS: {self.clock.get_fps() :.1f}' + ";"
        self.debug_text += ";"
        self.debug_text += "Player pos: " + str(round(self.player.x, 1)) + ", " + str(round(self.player.y, 1)) + ";"
        self.debug_text += "Player Angle: " + str(round(math.degrees(self.player.angle), 0)) + ";"
        self.debug_text += ";"
        self.debug_text += "Projectiles: " + str(len(self.projectile_handler.sprites)) + ";"

    def draw(self):
        self.object_renderer.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and self.togle_text == False:
                    self.togle_text = True
                elif event.key == pygame.K_p and self.togle_text == True:
                    self.togle_text = False

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = GAME()
    game.run()
