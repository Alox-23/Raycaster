import pygame
import item
import crosshair

class CrossItem(item.Item):
    def __init__(self, *args):
        super().__init__(*args)

        self.crosshair = crosshair.CrossHair(self.game, width= 200)
        self.range = 3

    def check_collision(self):
        for sprite in self.game.sprite_handler.sprites:
            try:
                if sprite[0].colliderect(self.crosshair.rect):
                    return sprite
            except:
                return None
        return None

    def check_range(self):
        self.crosshair.set_color((0, 0, 255))
        self.col_sprite = self.check_collision()
        self.useable = False
        if self.col_sprite != None and self.col_sprite[1].norm_dist < self.range and self.col_sprite[1].norm_dist > 0:
            self.crosshair.set_color((255, 0, 0))
            self.useable = True
            
    
    def update(self):
        super().update()
        self.check_range()