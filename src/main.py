import pygame
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite import *
from sprite_handler import *

class GAME:

    def __init__(self):
        pygame.init()
        self.screan = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.player = PLAYER(self)
        self.sprite_handler = SpriteHandler(self)
        self.object_renderer = ObjectRenderer(self)
        self.map = Map(self)
        self.raycasting = RayCasting(self)

    def load_screen(self):
        self.object_renderer.load_screen()

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.sprite_handler.update()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f} FPS')

    def draw(self):
        self.object_renderer.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                             and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = GAME()
    game.run()
