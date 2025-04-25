import pygame
from settings import *
import json

class ObjectRenderer:

    def __init__(self, game):
        
        self.game = game
        self.text_buffer = pygame.Surface((250, 150))
        #self.text_buffer.set_colorkey((0,0,0))
        self.rects_to_render = []
        self.fog_scale = -15
        self.fog_offset = 300
        self.resize_buffer = game.resize_buffer
        self.display = game.display 
        self.texture_path = "assets/textures/"
        self.wall_textures = self.load_wall_textures()
        self.door_textures = self.load_wall_textures()

        self.fog_color = FOG_COLOR

    def init_sky(self, sky_path = "sky.png", floor_color = FLOOR_COLOR, roof_color = (1,1,1, 255), fog_color = FOG_COLOR, fog_height = 200, fog_offset = 300, fog_scale = -15):
        if sky_path != 0:
            self.sky_image = self.get_texture(self.texture_path+sky_path, (WIDTH, HEIGHT))
        else:
            self.sky_image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
            self.sky_image.fill(roof_color)

        self.floor_image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
        self.floor_image.fill(floor_color)

        self.fog_height = fog_height
        self.fog_color = fog_color
        self.fog_offset = fog_offset
        self.fog_scale = fog_scale

        if sky_path != 0:
            for x in range(WIDTH):
                for y in range(HALF_HEIGHT):
                    a = self.sky_image.get_at((x, y))
                    a[3] = int(y / HALF_HEIGHT * 255)
                    self.sky_image.set_at((x, HEIGHT-y), a)

        else:
            for x in range(WIDTH):
                for y in range(self.fog_height):
                    a = self.sky_image.get_at((x, y))
                    if y % 2 == 0:
                        a[3] = int(y / self.fog_height * 255)
                    else:
                        a[3] = int((y-1) / self.fog_height * 255)
                    self.sky_image.set_at((x, HEIGHT-y), a)
        

        for x in range(WIDTH):
            for y in range(self.fog_height):
                a = self.floor_image.get_at((x, y))
                if y % 2 == 0:
                    a[3] = int(y / self.fog_height * 255)
                else:
                    a[3] = int((y-1) / self.fog_height * 255)
                self.floor_image.set_at((x, y), a)

        self.sky_offset = 0
        
    def draw_text(self):
        t = ""
        y_cntr = 0
        self.text_buffer.fill((0,0,255))
        for i in self.game.debug_text:
            if i != ";":
                t += i
            else:
                t_surf = self.game.font.render(t, False, (0,255,0))
                self.text_buffer.blit(t_surf, (5, 4+y_cntr*20))
                t = ""
                y_cntr += 1
        self.display.blit(self.text_buffer, (5,5))

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.game.hud.draw(self.resize_buffer)
        try:
            self.game.player.held_item.crosshair.draw(self.resize_buffer)
        except:
            pass
        self.draw_resize_buffer()
        if self.game.togle_text == True:
            self.draw_text()
        pygame.display.flip()

    def draw_resize_buffer(self):
        self.display.blit(
        pygame.transform.scale(self.resize_buffer, 
                               (
                                   self.display.get_width(), 
                                    self.display.get_height()
                                )
                                ),
                        
        (0,0)
        )

    def draw_background(self):
        self.resize_buffer.fill(self.fog_color)

        self.sky_offset = (8.0 * math.degrees(self.game.player.angle)) % WIDTH
        self.resize_buffer.blit(self.sky_image, (-self.sky_offset, -HALF_HEIGHT))
        self.resize_buffer.blit(self.sky_image, (-self.sky_offset + WIDTH, -HALF_HEIGHT))

        self.resize_buffer.blit(self.floor_image, (0, HALF_HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key = lambda t: t[0], reverse=True)
        for depth, img, pos in list_objects:
            self.resize_buffer.blit(img, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)
    
    @staticmethod
    def get_texture_from_tileset(path, pos = (0,-9), res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        tileset = pygame.image.load(path)
        image = pygame.Surface(res)
        image.blit(tileset, (pos[0]*res[0], pos[1]*res[1]))
        return image

    def load_wall_textures(self):
        with open("data/textures.json", "r") as f:
            data = json.load(f)
        
        data2 = {}
        for key, value in data.items():
            data2[int(key)] = self.get_texture(self.texture_path+value)
        return data2

    def load_resize_buffer(self):
        self.resize_buffer.blit(pygame.transform.scale(pygame.image.load("assets/loading.jpg"), RES), (0,0))