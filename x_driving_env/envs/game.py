import pygame
import sys
import random

from constants import *

from car import Car
from road import Road
from speed_sign import SpeedSign
from speed_bump import SpeedBump


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
        self.speed_bumps = []
        self.current_speed_limit = 25
        self.current_speed_sign_image = None
        self.generate_speed_signs()
        self.generate_speed_bumps()

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

            for bump in self.speed_bumps:
                bump.draw(self.screen, render=True)

            self.car.draw(self.screen)

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
        self.update_speed_bumps()

        # Update score only if below speed limit
        if self.car.velocity <= self.current_speed_limit + 1:
            self.score = (
                self.car.velocity + self.car.acceleration * 10 - PENALTY_CONSTANT
            )
        else:
            self.score = -self.car.acceleration * 10 - PENALTY_CONSTANT

        if self.car.on_kerbs():
            self.score -= 3 * PENALTY_CONSTANT
        elif self.car.on_grass():
            self.score -= 10 * PENALTY_CONSTANT

        self.score /= SCORE_NORMALIZE

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

    def generate_speed_bumps(self):
        distances = range(0, END_POINT_DISTANCE + 1, 1000)
        for d in distances:
            lane = random.choice(["left", "right"])
            if lane == "left":
                position = (ROAD_LEFT + 10, -d)
            else:
                position = (ROAD_RIGHT - 90, -d)
            self.speed_bumps.append(SpeedBump(position))

    def update_speed_bumps(self):
        for bump in self.speed_bumps:
            bump.position = (bump.position[0], bump.position[1] + self.car.velocity)
            bump.rect.y = bump.position[1]

            # Check if the car is near the sign
            if (
                self.car.rect.colliderect(bump.rect) and not bump.collided
            ):  # Threshold for proximity
                self.car.velocity *= 2 / 3
                bump.collided = True


if __name__ == "__main__":
    game = Game()
    game.run_game()
