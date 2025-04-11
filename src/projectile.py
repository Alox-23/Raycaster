import pygame
import sprite

class ProjectileObject(sprite.SpriteObject):
    def __init__(self, game, dir = (10.5, 3.5), path = "assets/sprites/goblin/pixil-frame-0.png",
                  pos = (10.5, 3.5), scale = 0.2, shift = -0.675):
        super().__init__(game, pos = pos, path = path, scale = scale, shift = shift)
        self.speed = 0.02
        self.fire(dir)
        
    def fire(self, direction):
        self.dx = direction.x*self.speed
        self.dy = direction.y*self.speed
    
    def check_wall(self):
        return (int(self.x), int(self.y)) in self.game.map.world_map[0]

    