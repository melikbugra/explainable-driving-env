import pygame
import sys
import random

from .constants import *

from .car import Car
from .road import Road
from .speed_sign import SpeedSign
from .speed_bump import SpeedBump


class Game:
    def __init__(self, bumps_activated=False, bump_env=False):
        self.screen = None  # Initialize without creating a Pygame window
        self.bumps_activated = bumps_activated
        self.bump_env = bump_env
        self.initial_state()
        self.rendering_set = False

    def setup_rendering(self):
        if not self.screen:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("3D Driving Game")
            self.clock = pygame.time.Clock()
            self.rendering_set = True

    def initial_state(self):
        self.time = 0  # Record the start time
        self.car = Car(self.bump_env)
        self.road = Road()
        self.distance_travelled = 0
        self.game_over = False
        self.reward = 0
        self.score = 0
        self.speed_signs = []
        self.speed_bumps = []
        self.speed_limits = [3, 5, 7, 10]
        self.current_speed_limit = 10
        self.next_bump_x_position = 0
        self.next_bump_y_position = 0
        self.current_speed_sign_image = None
        self.collided_a_bump: bool = False
        self.generate_speed_signs()
        if self.bumps_activated:
            self.generate_speed_bumps()

    def reset(self):
        self.initial_state()

        return self.get_state_representation()

    def render_text(self, text, position, color=(255, 255, 255)):
        font = pygame.font.SysFont(None, 36)
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, position)

    def run(self, render=False):
        if not self.rendering_set:
            self.setup_rendering()
        if render:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update and draw the game for one frame
            if not self.game_over:
                self.draw(render)
            # else:
            #     self.display_end_message()

    def run_game(self):
        while not self.game_over:
            self.update_game()
            state = self.get_state_representation()
            self.run(render=True)
            pygame.display.flip()
            self.clock.tick(60)

    def draw(self, render=False):
        if render:
            self.draw_grass()
            self.road.draw(self.screen)

            # Display velocity, acceleration, and reward
            self.render_text(f"Velocity: {self.car.velocity*10:.2f}", (10, 10))
            self.render_text(f"Acceleration: {self.car.acceleration*10:.3f}", (10, 50))
            self.render_text(
                f"Reward: {float(self.reward):.4f}", (10, 90)
            )  # Display reward
            self.render_text(
                f"Score: {float(self.score):.3f}", (10, 130)
            )  # Display reward

            # Draw the current speed sign image (smaller version) under the reward
            if self.current_speed_sign_image:
                self.screen.blit(
                    pygame.transform.scale(self.current_speed_sign_image, (40, 40)),
                    (10, 170),
                )

            for sign in self.speed_signs:
                sign.draw(self.screen, render=True)
            if self.bumps_activated:
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

    def update_game(self, long_action=None, lat_action=None):
        self.bump_collision_penalty = 0
        # Update the game state
        self.time += 1
        if self.time > MAX_GAME_TIME:
            self.game_over = True

        self.car.update(long_action, lat_action)
        self.road.update(self.car.velocity)
        self.distance_travelled += self.car.velocity
        self.update_speed_signs()
        if self.bumps_activated:
            self.update_speed_bumps()

        if self.car.velocity <= self.current_speed_limit:
            self.reward = 1 - (self.current_speed_limit - self.car.velocity) / (
                self.speed_limits[-1] - self.speed_limits[0]
            )
        else:
            self.reward = (self.current_speed_limit - self.car.velocity) / (
                self.speed_limits[-1] - self.speed_limits[0]
            )

        if self.bump_env:
            if self.car.on_kerbs():
                self.reward = -0.25
            elif self.car.on_grass():
                self.reward = -0.5

            if self.collided_a_bump:
                self.reward = -100

        self.reward /= REWARD_CONSTANT
        self.score += self.reward

        if self.distance_travelled >= END_POINT_DISTANCE:
            self.game_over = True

    def step(self, long_action, lat_action=None):
        self.update_game(long_action, lat_action)

        reward = self.reward

        done = self.game_over

        state = self.get_state_representation()
        info = {}

        return state, reward, done, info

    def get_state_representation(self):
        if self.bump_env:
            return {
                "car_speed": self.car.velocity,
                "current_speed_limit": self.current_speed_limit,
                "car_x_position": self.car.rect.centerx,
                "next_bump_x_position": self.next_bump_x_position,
                "next_bump_y_position": self.next_bump_y_position,
            }
        else:
            return {
                "car_speed": self.car.velocity,
                "current_speed_limit": self.current_speed_limit,
            }

    def display_end_message(self):
        # Display "Game Over" and final reward
        font = pygame.font.SysFont(None, 55)
        game_over_text = font.render("Game Over!", True, (0, 0, 0))
        reward_text = font.render(f"Final Score: {float(self.score)}", True, (0, 0, 0))

        game_over_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 - 30)
        )
        reward_rect = reward_text.get_rect(
            center=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 + 30)
        )

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(reward_text, reward_rect)

    def generate_speed_signs(self):
        distances = range(0, END_POINT_DISTANCE + 1, 5000)
        for d in distances:
            limit = random.choice(self.speed_limits)
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
        self.collided_a_bump = False
        for bump in self.speed_bumps:
            if bump.collided or bump.passed:
                pass
            bump.position = (bump.position[0], bump.position[1] + self.car.velocity)
            bump.rect.y = bump.position[1]

            if abs(self.car.rect.y - bump.rect.y) < 1000:  # Threshold for proximity
                self.next_bump_x_position = bump.rect.centerx
                self.next_bump_y_position = bump.rect.centery

            if self.car.rect.colliderect(bump.rect) and not bump.collided:
                self.bump_collision_penalty = -10
                self.collided_a_bump = True
                self.car.velocity *= 1 / 5
                bump.collided = True

            if self.car.rect.y < bump.rect.y:
                bump.passed = True


if __name__ == "__main__":
    game = Game()
    game.run_game()
