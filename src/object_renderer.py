import pygame
from settings import *


class ObjectRenderer:

    def __init__(self, game):
        self.game = game
        self.screen = game.screan
        self.texture_path = "assets/textures/"
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture(self.texture_path+"sky.png", (WIDTH, HEIGHT))
        self.sky_offset = 0

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        print(self.game.player.vert_angle)
        self.sky_offset = (8.0 * math.degrees(self.game.player.angle)) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0-self.game.player.vert_angle-HALF_HEIGHT))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0-self.game.player.vert_angle-HALF_HEIGHT))

        pygame.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT-self.game.player.vert_angle-50, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = self.game.ray.objects_to_render
        for depth, img, pos in list_objects:
            self.screen.blit(img, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture(self.texture_path+'wall.png'),
            2: self.get_texture(self.texture_path+'wall2.png'),
            3: self.get_texture(self.texture_path+"wall3.png")
        }
