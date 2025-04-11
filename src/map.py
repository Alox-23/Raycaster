import pygame
import json
import random

class Map:
    def __init__(self, game):
        self.game = game
        self.change_level("city.json")
        self.set_level()

    def set_level(self):
        self.world_map = self.active_level.level_map
    
    def get_data(self, level_path):
        with open(level_path, "r") as f:
            self.data = json.load(f)

    def check_player_door_collision(self, floor, x, y):
        if (x, y) in self.world_map[floor] and self.world_map[floor][(x, y)].value in self.data["doors"]:
            self.change_level(self.world_map[floor][(x,y)].level)

    def change_level(self, level_path, inside = False):
        self.game.object_renderer.load_resize_buffer()
        pygame.display.update()
        self.get_data("data/levels/"+level_path)
        self.active_level = Level(self.game, self.data)
        
        self.game.sprite_handler.load_sprites(self.data)
        self.game.projectile_handler.clear_all()
        self.game.player.change_pos(self.data["player-pos"])
        self.game.object_renderer.init_sky(sky_path = self.data["sky"], roof_color = self.data["roof-color"], fog_color = self.data["fog-color"], floor_color = self.data["floor-color"], fog_height = self.data["fog-height"], fog_scale = self.data["fog-scale"], fog_offset = self.data["fog-offset"])
        self.set_level()

class Level:
    def __init__(self, game, data):
        self.game = game
        self.data = data
        self.mini_map =  data["level"]
        self.level_map = {}
        self.get_level()

    def get_level(self):
        for floor_num, floor in enumerate(self.mini_map):
            self.level_map[floor_num] = {}
            for j, row in enumerate(floor):
                for i, value, in enumerate(row):
                
                    if value in self.data["doors"]:
                        self.level_map[floor_num][(i, j)] = Door(value, self.data["door-level"][str(value)])

                    elif value:
                        self.level_map[floor_num][(i, j)] = Tile(value)

class Tile:
    def __init__(self, value):
        self.value = value

class Door(Tile):
    def __init__(self, value, level = None):
        self.value = value
        self.level = level