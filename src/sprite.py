import pygame
from settings import *

class SpriteObject:
    def __init__(self, game, path = "assets/sprites/goblin/wall.png",
                  pos = (10.5, 3.5), scale = 1, shift = 0):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pygame.image.load(path).convert_alpha()
        self.draw_image = self.image
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.resize_buffer_x, self.dist, self.norm_dist = 0, 0, 0, 0, 0, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        #(ray * SCALE, HALF_HEIGHT - ((floor-self.game.player.z+1) * proj_height))
        proj = resize_buffer_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pygame.transform.scale(self.image, (proj_width, proj_height))
        self.draw_image = image
        self.sprite_half_width = proj_width // 2
        pos = self.resize_buffer_x - self.sprite_half_width, HALF_HEIGHT - ((self.SPRITE_HEIGHT_SHIFT-self.game.player.z+1) * proj_height)
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))
        

    def get_sprite(self):
        
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau
        
        delta_rays = delta / DELTA_ANGLE
        self.resize_buffer_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if - self.IMAGE_HALF_WIDTH < self.resize_buffer_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()
            

    def update(self):
        self.x+=self.dx*self.game.delta_time
        self.y+=self.dy*self.game.delta_time
        self.get_sprite()
