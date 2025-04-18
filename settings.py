"""
Game settings and constants
"""

# Screen settings
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Pixel Platformer"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BG_COLOR = (69, 40, 60)  # Dark purple-ish background

# Game settings
TILE_SIZE = 32
GRAVITY = 0.7
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = 0.12
PLAYER_JUMP_FORCE = -16
MAX_FALL_SPEED = 20

# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_LEVEL_COMPLETE = 3

# Asset paths
ASSETS_DIR = "assets"
SPRITES_DIR = f"{ASSETS_DIR}/sprites"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"

# Level layouts
LEVEL_1 = [
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "    P                  E        ",
    "XXXXXXXX     XXXXXX    XXXXXXXX",
    "       XX            XXX       ",
    "        XX    C     XX         ",
    "         XXXXXXXXXXXXX         ",
    "                                ",
    "                                ",
    "                                ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_2 = [
    "                                ",
    "                                ",
    "                                ",
    "     C      C      C      C    ",
    "                                ",
    "  XXXXXXX  XXXXX  XXXXX  XXXXX ",
    "                                ",
    "                             E  ",
    "P                          XXXX",
    "XXXX   XX     XX    XX         ",
    "    XXXXX    XXXX  XXXX     C  ",
    "                          XXXXX",
    "                                ",
    "            C  C  C            ",
    "          XXXXXXXXXXXX         ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVELS = [LEVEL_1, LEVEL_2]