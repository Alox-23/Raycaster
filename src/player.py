from settings import *
import pygame
import math
 
class PLAYER:
    def __init__(self, game):
        self.game = game
        self.speed = 0.01
        self.x, self.y = PLAYER_POS
        self.z = 0.5
        self.angle = PLAYER_ANGLE
        self.floor = 0
        self.projectile_timer = 0
        self.projectile_interval = 100

        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.max_mana = 100
        self.stamina = 100
        self.max_stamina = 100

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map[self.floor]

    def check_wall_collision(self):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + self.dx * scale), int(self.y)):
            self.x += self.dx
        if self.check_wall(int(self.x), int(self.y + self.dy * scale)):
            self.y += self.dy
        
        self.game.map.check_player_door_collision(self.floor, int(self.x + self.dx * scale), int(self.y + self.dy * scale))

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        self.dx, self.dy = 0, 0
        speed = self.speed * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.dx += speed_cos
            self.dy += speed_sin
        if keys[pygame.K_s]:
            self.dx += -speed_cos
            self.dy += -speed_sin
        if keys[pygame.K_a]:
            self.dx += speed_sin
            self.dy += -speed_cos
        if keys[pygame.K_d]:
            self.dx += -speed_sin
            self.dy += speed_cos

        #self.game.projectile_handler.fire(pygame.math.Vector2(self.x, self.y), pygame.math.Vector2(math.cos(self.angle), math.sin(self.angle)))

        self.check_wall_collision()

        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau

    def draw(self):
        pygame.draw.circle(self.game.screan, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()
    
    def change_pos(self, pos):
        self.y = pos[1]
        self.x = pos[0]
    
    def draw_hands(self, d):
        d.blit(self.player_hands, self.player_hands_rect)

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

