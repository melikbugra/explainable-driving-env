# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAX_GAME_TIME = 2500

ROAD_MAX_VELOCITY = 10
KERB_MAX_VELOCITY = 7
GRASS_MAX_VELOCITY = 4

END_POINT_DISTANCE = (
    MAX_GAME_TIME * ROAD_MAX_VELOCITY * 1000
)  # Distance to reach for the game to end
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

REWARD_NORMALIZE = 1000
PENALTY_CONSTANT = 1

# Constants for car movement
ACCELERATION = 0.05  # Acceleration value when the up key is pressed
DECELERATION = 0.05  # Deceleration value when the down key is pressed

ROAD_MIN_FREE_DECEL = 0.01
KERB_MIN_FREE_DECEL = 0.01
GRASS_MIN_FREE_DECEL = 0.01

ROAD_FRICTION = 0.003  # Existing friction value, used for the road
KERB_FRICTION = 0.008  # Higher friction for kerbs
GRASS_FRICTION = 0.009  # Even higher friction for grass
