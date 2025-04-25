import pygame
import sprites.sprite
import math

class ProjectileObject(sprites.sprite.SpriteObject):
    def __init__(self, game, dir = (10.5, 3.5), path = "assets/sprites/goblin/pixil-frame-0.png",
                  pos = (10.5, 3.5), scale = 0.2, shift = -0.675):
        super().__init__(game, pos = pos, path = path, scale = scale, shift = shift)
        self.speed = 0.001
        self.damage = 30
        self.size = 0.4
        self.fire(dir)
        
    def fire(self, direction):
        self.dx = direction.x*self.speed * self.game.delta_time
        self.dy = direction.y*self.speed * self.game.delta_time

    def update(self):
        super().update()
        return self.check_collision()
    
    def check_wall(self):
        return (int(self.x), int(self.y)) in self.game.map.world_map[0]
    
    def check_collision(self):
        for sprite in self.game.sprite_handler.sprites:
            sprite_x = sprite[1].x
            sprite_y = sprite[1].y

            if abs(sprite_x - self.x) < self.size and abs(sprite_y - self.y) < self.size:
                sprite[1].health -= self.damage
                return True
        return False

    