from settings import *
import pygame
import math
 
class PLAYER:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.vert_angle = 0
        self.floor = 0

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map[self.floor]

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
        
        self.game.map.check_player_door_collision(self.floor, int(self.x + dx * scale), int(self.y + dy * scale))

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pygame.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pygame.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        if keys[pygame.K_UP] and self.vert_angle >= -220:
            self.vert_angle -= PLAYER_VERT_ROT_SPEED * self.game.delta_time
        if keys[pygame.K_DOWN] and self.vert_angle <= 170:
            self.vert_angle += PLAYER_VERT_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    def draw(self):
        pygame.draw.circle(self.game.screan, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()
    
    def change_pos(self, pos):
        self.y = pos[1]
        self.x = pos[0]

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

