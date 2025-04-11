from settings import *
import pygame
import math
 
class PLAYER:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.z = 0
        self.angle = PLAYER_ANGLE
        self.vert_angle = 0
        self.floor = 0
        self.projectile_timer = 0
        self.projectile_interval = 600
        self.player_hands = pygame.image.load("assets/sprites/hands.png")
        self.player_hands = pygame.transform.scale(self.player_hands, (150, 150))
        self.player_hands_rect = self.player_hands.get_rect()
        self.player_hands_rect.center = (HALF_WIDTH, HEIGHT-75)

        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.max_mana = 100
        self.stamina = 100
        self.max_stamina = 100

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

        if keys[pygame.K_SPACE] and self.projectile_timer> self.projectile_interval:
            self.projectile_timer = 0
            self.mana-= 10
            self.health-= 10
            self.stamina-= 10
            self.player_hands_rect.centery =  HEIGHT-75
            self.game.projectile_handler.fire(pygame.math.Vector2(self.x, self.y), pygame.math.Vector2(math.cos(self.angle), math.sin(self.angle)))

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
        if not self.projectile_timer > self.projectile_interval:
            self.player_hands_rect.centery += 1
            self.projectile_timer += 1 * self.game.delta_time
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

