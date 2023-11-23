import pygame
import sys
import random

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

SCORE_NORMALIZE = 100


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


class Game:
    def __init__(self):
        self.screen = None  # Initialize without creating a Pygame window
        self.initial_state()

    def setup_rendering(self):
        if not self.screen:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("3D Driving Game")
            self.clock = pygame.time.Clock()

    def initial_state(self):
        self.time = 0  # Record the start time
        self.car = Car()
        self.road = Road()
        self.distance_travelled = 0
        self.game_over = False
        self.score = 0
        self.speed_signs = []
        self.current_speed_limit = 25
        self.current_speed_sign_image = None
        self.generate_speed_signs()

    def reset(self):
        self.initial_state()

    def render_text(self, text, position, color=(255, 255, 255)):
        font = pygame.font.SysFont(None, 36)
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, position)

    def run(self, render=False):
        if render:
            self.setup_rendering()
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update and draw the game for one frame
            if not self.game_over:
                self.draw(render)
            else:
                self.display_end_message()

    def run_game(self):
        self.setup_rendering()
        while not self.game_over:
            self.update_game()
            self.run(render=True)
            pygame.display.flip()
            self.clock.tick(60)

    def draw(self, render=False):
        if render:
            self.setup_rendering()
            self.draw_grass()
            self.road.draw(self.screen)
            self.car.draw(self.screen)

            # Display velocity, acceleration, and score
            self.render_text(f"Velocity: {self.car.velocity:.2f}", (10, 10))
            self.render_text(f"Acceleration: {self.car.acceleration:.3f}", (10, 50))
            self.render_text(
                f"Score: {float(self.score):.3f}", (10, 90)
            )  # Display score

            # Draw the current speed sign image (smaller version) under the score
            if self.current_speed_sign_image:
                self.screen.blit(
                    pygame.transform.scale(self.current_speed_sign_image, (40, 40)),
                    (10, 130),
                )

            for sign in self.speed_signs:
                sign.draw(self.screen, render=True)

    def draw_grass(self):
        # Draw grass on the left side of the road
        left_grass_rect = pygame.Rect(0, 0, GRASS_LEFT, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, GRASS_COLOR, left_grass_rect)

        # Draw grass on the right side of the road
        right_grass_rect = pygame.Rect(
            GRASS_RIGHT, 0, SCREEN_WIDTH - GRASS_RIGHT, SCREEN_HEIGHT
        )
        pygame.draw.rect(self.screen, GRASS_COLOR, right_grass_rect)

    def update_game(self, action=None):
        # Update the game state
        self.time += 1
        if self.time > MAX_GAME_TIME:
            self.game_over = True

        self.car.update(action)
        self.road.update(self.car.velocity)
        self.distance_travelled += self.car.velocity
        self.update_speed_signs()

        # Update score only if below speed limit
        if self.car.velocity <= self.current_speed_limit + 1:
            self.score = (
                self.car.velocity + self.car.acceleration * 10
            ) / SCORE_NORMALIZE - 0.001
        else:
            self.score = (-self.car.acceleration * 10) / SCORE_NORMALIZE - 0.001

        if self.distance_travelled >= END_POINT_DISTANCE:
            self.game_over = True

    def step(self, action):
        # Apply an action and update the game state
        self.update_game(action)

        # Calculate reward (this is just an example, adjust as needed)
        reward = self.score  # or any other logic for reward calculation

        # Check if the game is over
        done = self.game_over

        # Return the new state, reward, done, and any additional info
        # State can be a representation of the game state (e.g., position of car, velocity, etc.)
        state = self.get_state_representation()
        info = {}  # Additional info if needed

        return state, reward, done, info

    def get_state_representation(self):
        # This method should return the current state of the game
        # For example, it could be the position of the car, its velocity, distance travelled, etc.
        # Adjust this method based on what state representation you need for your RL environment
        return {
            "car_position": self.car.rect.center,
            "velocity": self.car.velocity,
            "distance_travelled": self.distance_travelled,
            "current_speed_limit": self.current_speed_limit,
        }

    def display_end_message(self):
        # Display "Game Over" and final score
        font = pygame.font.SysFont(None, 55)
        game_over_text = font.render("Game Over!", True, (0, 0, 0))
        score_text = font.render(f"Final Score: {float(self.score)}", True, (0, 0, 0))

        game_over_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 - 30)
        )
        score_rect = score_text.get_rect(
            center=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 + 30)
        )

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)

    def generate_speed_signs(self):
        distances = range(0, END_POINT_DISTANCE + 1, 5000)
        for d in distances:
            limit = random.choice([3, 5, 7, 10, 15])
            position = (SCREEN_WIDTH // 2 + ROAD_WIDTH - 20, -d)
            self.speed_signs.append(SpeedSign(limit, position))

    def update_speed_signs(self):
        for sign in self.speed_signs:
            sign.position = (sign.position[0], sign.position[1] + self.car.velocity)
            sign.rect.y = sign.position[1]

            # Check if the car is near the sign
            if abs(self.car.rect.y - sign.rect.y) < 100:  # Threshold for proximity
                self.current_speed_limit = sign.limit
                self.current_speed_sign_image = (
                    sign.image
                )  # Update the current speed sign image


class Car:
    def __init__(self):
        self.size = (50, 100)
        self.image = pygame.Surface(
            self.size, pygame.SRCALPHA
        )  # Use SRCALPHA for transparency
        self.color = (0, 0, 255)  # Blue car

        # Draw the car body
        pygame.draw.rect(self.image, self.color, (0, 0, self.size[0], self.size[1]))

        # Draw windows (glasses) and bodywork
        pygame.draw.rect(self.image, (135, 206, 235), (10, 10, 30, 20))  # Front window
        pygame.draw.rect(self.image, (135, 206, 235), (10, 60, 30, 20))  # Rear window
        pygame.draw.line(self.image, (0, 0, 0), (10, 40), (40, 40), 2)  # Bodywork line

        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))

        self.velocity = 0
        self.acceleration = 0
        self.turn_angle = 0  # Angle for turning the tires

        # Tires
        self.tire_width, self.tire_height = 8, 20  # Narrower tires
        self.front_tires = [
            pygame.Surface((self.tire_width, self.tire_height), pygame.SRCALPHA),
            pygame.Surface((self.tire_width, self.tire_height), pygame.SRCALPHA),
        ]
        for tire in self.front_tires:
            tire.fill((0, 0, 0))  # Black tires

    def update(self, action=None):
        if action is not None:
            # Handle actions programmatically
            self.handle_action(action)
        else:
            # Handle keyboard input
            self.handle_keyboard_input()

    def handle_action(self, action):
        move_speed = 2  # Speed of lateral movement (should be int)
        self.turn_angle = 0  # Reset tire angle

        if action == 1:
            self.rect.x -= move_speed
            self.rect.x = max(self.rect.x, 0)  # Prevent moving off-screen to the left
            self.turn_angle = 30  # Turn tires left
        if action == 3:
            self.rect.x += move_speed
            right_edge = SCREEN_WIDTH - self.rect.width
            self.rect.x = min(
                self.rect.x, right_edge
            )  # Prevent moving off-screen to the right
            self.turn_angle = -30  # Turn tires right
        if action == 2:
            self.acceleration = ACCELERATION
            if self.on_grass():
                self.acceleration -= GRASS_FRICTION
                if self.velocity > GRASS_MAX_VELOCITY:
                    self.acceleration = -GRASS_FRICTION
            elif self.on_kerbs():
                self.acceleration -= KERB_FRICTION
                if self.velocity > KERB_MAX_VELOCITY:
                    self.acceleration = -KERB_FRICTION
            elif self.on_road():
                self.acceleration -= ROAD_FRICTION
        elif action == 4:
            self.acceleration = -DECELERATION
            if self.on_grass():
                self.acceleration -= GRASS_FRICTION
            elif self.on_kerbs():
                self.acceleration -= KERB_FRICTION
            elif self.on_road():
                self.acceleration -= ROAD_FRICTION

            if self.velocity == 0:
                self.acceleration = 0
        else:
            # Determine the surface and apply corresponding friction
            self.acceleration = 0.0
            if self.on_grass():
                if self.acceleration > -GRASS_MIN_FREE_DECEL:
                    self.acceleration -= GRASS_FRICTION
                else:
                    self.acceleration = -GRASS_MIN_FREE_DECEL
            elif self.on_kerbs():
                if self.acceleration > -KERB_MIN_FREE_DECEL:
                    self.acceleration -= KERB_FRICTION
                else:
                    self.acceleration = -KERB_MIN_FREE_DECEL
            elif self.on_road():
                if self.acceleration > -ROAD_MIN_FREE_DECEL:
                    self.acceleration -= ROAD_FRICTION
                else:
                    self.acceleration = -ROAD_MIN_FREE_DECEL

            if self.velocity == 0:
                self.acceleration = 0

        # Update velocity based on acceleration
        self.velocity += self.acceleration
        self.velocity = max(0, min(self.velocity, ROAD_MAX_VELOCITY))

    def handle_keyboard_input(self):
        keys = pygame.key.get_pressed()
        move_speed = 2  # Speed of lateral movement (should be int)
        self.turn_angle = 0  # Reset tire angle
        if keys[pygame.K_LEFT]:
            self.rect.x -= move_speed
            self.rect.x = max(self.rect.x, 0)  # Prevent moving off-screen to the left
            self.turn_angle = 30  # Turn tires left
        if keys[pygame.K_RIGHT]:
            self.rect.x += move_speed
            right_edge = SCREEN_WIDTH - self.rect.width
            self.rect.x = min(
                self.rect.x, right_edge
            )  # Prevent moving off-screen to the right
            self.turn_angle = -30  # Turn tires right
        if keys[pygame.K_UP]:
            self.acceleration = ACCELERATION
            if self.on_grass():
                self.acceleration -= GRASS_FRICTION
                if self.velocity > GRASS_MAX_VELOCITY:
                    self.acceleration = -GRASS_FRICTION
            elif self.on_kerbs():
                self.acceleration -= KERB_FRICTION
                if self.velocity > KERB_MAX_VELOCITY:
                    self.acceleration = -KERB_FRICTION
            elif self.on_road():
                self.acceleration -= ROAD_FRICTION
        elif keys[pygame.K_DOWN]:
            self.acceleration = -DECELERATION
            if self.on_grass():
                self.acceleration -= GRASS_FRICTION
            elif self.on_kerbs():
                self.acceleration -= KERB_FRICTION
            elif self.on_road():
                self.acceleration -= ROAD_FRICTION

            if self.velocity == 0:
                self.acceleration = 0
        else:
            # Determine the surface and apply corresponding friction
            self.acceleration = 0.0
            if self.on_grass():
                if self.acceleration > -GRASS_MIN_FREE_DECEL:
                    self.acceleration -= GRASS_FRICTION
                else:
                    self.acceleration = -GRASS_MIN_FREE_DECEL
            elif self.on_kerbs():
                if self.acceleration > -KERB_MIN_FREE_DECEL:
                    self.acceleration -= KERB_FRICTION
                else:
                    self.acceleration = -KERB_MIN_FREE_DECEL
            elif self.on_road():
                if self.acceleration > -ROAD_MIN_FREE_DECEL:
                    self.acceleration -= ROAD_FRICTION
                else:
                    self.acceleration = -ROAD_MIN_FREE_DECEL

            if self.velocity == 0:
                self.acceleration = 0

        # Update velocity based on acceleration
        self.velocity += self.acceleration
        self.velocity = max(0, min(self.velocity, ROAD_MAX_VELOCITY))

    def draw(self, screen):
        # Draw the car body
        screen.blit(self.image, self.rect)

        # Draw and rotate front tires
        tire_positions = [(-2, 5), (44, 5)]  # Front left and right tire positions
        for i, tire in enumerate(self.front_tires):
            rotated_tire = pygame.transform.rotate(tire, self.turn_angle)
            tire_rect = rotated_tire.get_rect(
                center=(
                    self.rect.x + tire_positions[i][0] + self.tire_width // 2,
                    self.rect.y + tire_positions[i][1] + self.tire_height // 2,
                )
            )
            screen.blit(rotated_tire, tire_rect.topleft)

        # Draw rear tires (not rotating)
        rear_tire_positions = [(-2, 75), (44, 75)]  # Rear left and right tire positions
        for pos in rear_tire_positions:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.rect.x + pos[0],
                    self.rect.y + pos[1],
                    self.tire_width,
                    self.tire_height,
                ),
            )

    def on_road(self):
        # Check if all corners of the car are on the road
        return all(self.is_point_on_road(point) for point in self.get_car_corners())

    def on_kerbs(self):
        # Check if any corner of the car is on the kerbs
        return any(self.is_point_on_kerbs(point) for point in self.get_car_corners())

    def on_grass(self):
        # Check if any corner of the car is on the grass
        return any(self.is_point_on_grass(point) for point in self.get_car_corners())

    def get_car_corners(self):
        return [
            (self.rect.left, self.rect.top),
            (self.rect.right, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom),
        ]

    def is_point_on_road(self, point):
        x, y = point
        return ROAD_LEFT <= x <= ROAD_RIGHT

    def is_point_on_kerbs(self, point):
        x, y = point
        return (GRASS_LEFT < x < ROAD_LEFT) or (ROAD_RIGHT < x < GRASS_RIGHT)

    def is_point_on_grass(self, point):
        x, y = point
        return x <= GRASS_LEFT or x >= GRASS_RIGHT


class Road:
    def __init__(self):
        self.stripe_width = 10
        self.stripe_height = 100
        self.stripe_margin = 20
        self.stripe_speed = 5
        self.stripe_group_spacing = self.stripe_height + self.stripe_margin
        self.stripes = []
        for i in range(0, SCREEN_HEIGHT, self.stripe_group_spacing):
            for j in range(3):  # Create 3 stripes in each group
                self.stripes.append(i + (self.stripe_height + self.stripe_margin) * j)

        self.kerbs_left = self.initialize_kerbs()
        self.kerbs_right = self.initialize_kerbs()
        self.kerb_offset = 0

    def update(self, speed):
        # Update stripes
        for i in range(len(self.stripes)):
            self.stripes[i] += speed
            if self.stripes[i] > SCREEN_HEIGHT:
                self.stripes[i] -= SCREEN_HEIGHT + self.stripe_group_spacing

        # Update kerbs with the same logic
        self.kerb_offset += speed
        if self.kerb_offset >= KERB_HEIGHT:
            self.cycle_kerbs()
            self.kerb_offset -= KERB_HEIGHT

    def cycle_kerbs(self):
        # Cycle the kerb colors
        next_color_index = 1 if self.kerbs_left[0] == KERB_COLORS[0] else 0
        self.kerbs_left.insert(0, KERB_COLORS[next_color_index])
        self.kerbs_left.pop()

        next_color_index = 1 if self.kerbs_right[0] == KERB_COLORS[0] else 0
        self.kerbs_right.insert(0, KERB_COLORS[next_color_index])
        self.kerbs_right.pop()

    def draw(self, screen):
        # Draw the road
        road_rect = pygame.Rect(ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, ASPHALT_COLOR, road_rect)

        # Draw the stripes
        for stripe in self.stripes:
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (
                    SCREEN_WIDTH // 2 - self.stripe_width // 2,
                    stripe,
                    self.stripe_width,
                    self.stripe_height,
                ),
            )

        # Draw kerbs
        for y in range(-KERB_HEIGHT, SCREEN_HEIGHT, KERB_HEIGHT):
            kerb_color_left = self.kerbs_left[
                (y // KERB_HEIGHT + int(self.kerb_offset) // KERB_HEIGHT)
                % len(self.kerbs_left)
            ]
            kerb_color_right = self.kerbs_right[
                (y // KERB_HEIGHT + int(self.kerb_offset) // KERB_HEIGHT)
                % len(self.kerbs_right)
            ]
            pygame.draw.rect(
                screen,
                kerb_color_left,
                (
                    GRASS_LEFT,
                    y + int(self.kerb_offset) % KERB_HEIGHT,
                    KERB_WIDTH,
                    KERB_HEIGHT,
                ),
            )
            pygame.draw.rect(
                screen,
                kerb_color_right,
                (
                    ROAD_RIGHT,
                    y + int(self.kerb_offset) % KERB_HEIGHT,
                    KERB_WIDTH,
                    KERB_HEIGHT,
                ),
            )

    def initialize_kerbs(self):
        kerbs = []
        for y in range(0, SCREEN_HEIGHT // KERB_WIDTH):
            kerbs.append(KERB_COLORS[y % 2])  # Alternating red and white
        return kerbs


class SpeedSign:
    def __init__(self, limit, position):
        self.limit = limit
        self.position = position
        self.size = (80, 80)
        self.image = None
        self.rect = pygame.Rect(position[0], position[1], self.size[0], self.size[1])

    def create_image(self):
        # Create the image only when needed
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(
            self.image, (255, 255, 255), (40, 40), 40
        )  # White background
        pygame.draw.circle(self.image, (255, 0, 0), (40, 40), 40, 10)  # Red circle
        font = pygame.font.SysFont(None, 42)
        text = font.render(str(self.limit), True, (0, 0, 0))
        text_rect = text.get_rect(center=(40, 40))
        self.image.blit(text, text_rect)

    def draw(self, screen, render=False):
        if render:
            if not self.image:
                self.create_image()
            screen.blit(self.image, self.rect.topleft)


if __name__ == "__main__":
    game = Game()
    game.run_game()
