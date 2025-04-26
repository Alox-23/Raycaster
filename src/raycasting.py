import math
import pygame
from settings import *


class RayCasting:

    def __init__(self, game):
        self.game = game
        self.ray_casting_result = {}
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        floor = len(self.game.map.world_map)-1
        for i in range(len(self.game.map.world_map)):
            for ray, values in enumerate(self.ray_casting_result[floor]):
                depth, proj_height, texture, offset = values
                if depth < MAX_DEPTH-(MAX_DEPTH//5):
                    wall_column_text = self.textures[texture].subsurface(
                        offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE)
                    wall_column_text = pygame.transform.scale(wall_column_text,
                                                        (SCALE, proj_height))

                    wall_column_dark = self.textures[texture].subsurface(
                        offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE)
                    wall_column_dark = pygame.transform.scale(wall_column_dark,
                                                        (SCALE, proj_height))
                    wall_column_dark.fill(self.game.object_renderer.fog_color)
                    
                    wall_pos = (ray * SCALE, HALF_HEIGHT - ((floor/1.03-self.game.player.z+1) * proj_height))

                    if depth*self.game.object_renderer.fog_scale + self.game.object_renderer.fog_offset < 1:
                        wall_column_text.set_alpha(1)
                    else:
                        wall_column_text.set_alpha(depth*self.game.object_renderer.fog_scale + self.game.object_renderer.fog_offset)

                    wall_column = pygame.Surface((SCALE, proj_height))

                    wall_column.blit(wall_column_dark, (0,0))
                    wall_column.blit(wall_column_text, (0,0))

                    wall_column.set_colorkey(self.game.object_renderer.fog_color)

                    self.objects_to_render.append((depth, wall_column, wall_pos))
            floor -= 1

    def cast_one_ray(self, map, ox, oy, x_map, y_map, ray_angle, ray_num = 0):
        texture_hor, texture_vert = 1, 1
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        #horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor in map:
                texture_hor = map[tile_hor].value
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        #verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert in map:
                texture_vert = map[tile_vert].value
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        #depth
        if depth_vert < depth_hor:
            depth, texture = depth_vert, texture_vert
            y_vert %= 1
            offset = y_vert if cos_a > 0 else (1 - y_vert)
        else:
            depth, texture = depth_hor, texture_hor
            x_hor %= 1
            offset = (1 - x_hor) if sin_a > 0 else x_hor

        #remove fishbowl effect
        depth *= math.cos(self.game.player.angle - ray_angle)

        proj_height = resize_buffer_DIST / (depth + 0.0001)

        if proj_height < 0:
            return(depth, 1, texture, offset)

        return (depth, proj_height, texture, offset)

    def numba_cast(self, map, ox, oy, x_map, y_map, start_angle, num_rays = NUM_RAYS):
        ray_casting_result = []
        m = map
        ox, oy, x_map, y_map, ray_angle, num_rays = ox, oy, x_map, y_map, start_angle, num_rays
        
        for ray in range(num_rays):
            ray_casting_result.append(self.cast_one_ray(m, ox, oy, x_map, y_map, ray_angle, ray_num=ray))
            ray_angle += DELTA_ANGLE
        return ray_casting_result

    def ray_cast(self, map):
        ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001

        texture_vert, texture_hor = 1, 1
        for ray in range(NUM_RAYS):

            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            #horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in map:
                    texture_hor = map[tile_hor].value
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            #verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in map:
                    texture_vert = map[tile_vert].value
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            #depth
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)

            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            #remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            proj_height = resize_buffer_DIST / (depth + 0.0001)

            ray_casting_result.append(
                (depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE
        return ray_casting_result

    def update(self):
        for i in range(len(self.game.map.world_map)):
            #self.ray_casting_result[i] = self.ray_cast(self.game.map.world_map[i])
            self.ray_casting_result[i] = self.numba_cast(self.game.map.world_map[i], self.game.player.x, self.game.player.y, int(self.game.player.x), int(self.game.player.y), self.game.player.angle - HALF_FOV + 0.0001)
        
        self.get_objects_to_render()
