# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAX_GAME_TIME = 2000

# Road Related
ROAD_WIDTH = 200
ASPHALT_COLOR = (70, 70, 70)

KERB_WIDTH = 20
KERB_HEIGHT = 50
KERB_COLORS = [(255, 0, 0), (255, 255, 255)]

GRASS_WIDTH = (SCREEN_WIDTH - (ROAD_WIDTH + KERB_WIDTH * 2)) / 2
GRASS_COLOR = (0, 100, 0)

# Car Related
MIN_SPEED = 1

ACCELERATION = 0.05  # Acceleration value when the up key is pressed
DECELERATION = 0.05  # Deceleration value when the down key is pressed

ROAD_MIN_FREE_DECEL = 0.01
KERB_MIN_FREE_DECEL = 0.01
GRASS_MIN_FREE_DECEL = 0.01

ROAD_FRICTION = 0.003  # Existing friction value, used for the road
KERB_FRICTION = 0.008  # Higher friction for kerbs
GRASS_FRICTION = 0.009  # Even higher friction for grass

ROAD_MAX_VELOCITY = 10
KERB_MAX_VELOCITY = 7
GRASS_MAX_VELOCITY = 4
