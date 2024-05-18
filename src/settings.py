import math

RES = WIDTH, HEIGHT = 800, 450
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT// 2
FPS = 300

PLAYER_POS = 1.5, 5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.006
PLAYER_ROT_SPEED = 0.003
PLAYER_VERT_ROT_SPEED = 1
PLAYER_SIZE_SCALE = 120

FLOOR_COLOR = (30, 30, 30)

FOV = 1.2
HALF_FOV = FOV / 2
NUM_RAYS = 200
HALF_NUM_RAYS = NUM_RAYS // 4
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 30

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 150
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2