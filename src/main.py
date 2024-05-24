import pygame
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite import *

class GAME:

    def __init__(self):
        pygame.init()
        self.screan = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.new_game()
        self.delta_time = 1

    def new_game(self):
        self.map = Map(self)
        self.player = PLAYER(self)
        self.object_renderer = ObjectRenderer(self, self.map.data)
        self.raycasting = RayCasting(self)
        self.static_sprite = SpriteObject(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.static_sprite.update()
        pygame.display.flip()
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
