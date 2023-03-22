import pygame

_ = False
mini_map = [[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
             [1, _, _, 1, _, _, _, _, _, _, 1, 1, _, _, _, 1],
             [1, _, _, 1, _, _, _, _, _, _, 1, _, _, _, _, 1],
             [1, _, _, _, _, 1, 1, _, _, _, 1, _, _, _, _, 1],
             [1, _, _, _, _, _, 1, _, _, _, 1, _, _, _, _, 1],
             [1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, 1],
             [1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],

            [[1, 1, 1, 1, 1, 1, 1, _, _, _, _, _, _, _, _, _],
             [1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
             [1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
             [1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
             [1, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, 1],
             [1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, 1],
             [1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, 1],
             [1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]]


class Map:

    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()
        print(self.world_map[1])
        print(self.world_map)

    def get_map(self):
        for floor_num, floor in enumerate(self.mini_map):
            self.world_map[floor_num] = {}
            for j, row in enumerate(floor):
                for i, value, in enumerate(row):
                    if value:
                        self.world_map[floor_num][(i, j)] = value