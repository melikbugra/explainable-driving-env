# Constants
MAX_GAME_TIME = 1000  # 30 seconds in milliseconds

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
END_POINT_DISTANCE = 10000  # Distance to reach for the game to end
ASPHALT_COLOR = (70, 70, 70)  # Dark grey color for the road
GRASS_COLOR = (0, 100, 0)  # Darker shades of green
GRASS_SIZE = 50  # Size of each grass square
STRIPE_SPEED = 1.4  # Speed of road stripes, also used for grass speed
KERB_COLORS = [(255, 0, 0), (255, 255, 255)]  # Red and White for kerbs
ROAD_WIDTH = 200
ROAD_LEFT = SCREEN_WIDTH // 2 - ROAD_WIDTH // 2
ROAD_RIGHT = SCREEN_WIDTH // 2 + ROAD_WIDTH // 2
KERB_WIDTH = 20
KERB_HEIGHT = 50
GRASS_LEFT = ROAD_LEFT - KERB_WIDTH
GRASS_RIGHT = ROAD_RIGHT + KERB_WIDTH

SCORE_NORMALIZE = 1000
PENALTY_CONSTANT = 0.1

# Constants for car movement
ACCELERATION = 0.1  # Acceleration value when the up key is pressed
DECELERATION = 0.1  # Deceleration value when the down key is pressed

ROAD_MIN_FREE_DECEL = 0.025
KERB_MIN_FREE_DECEL = 0.025
GRASS_MIN_FREE_DECEL = 0.025

ROAD_FRICTION = 0.03  # Existing friction value, used for the road
KERB_FRICTION = 0.08  # Higher friction for kerbs
GRASS_FRICTION = 0.09  # Even higher friction for grass

ROAD_MAX_VELOCITY = 15
KERB_MAX_VELOCITY = 10
GRASS_MAX_VELOCITY = 3
