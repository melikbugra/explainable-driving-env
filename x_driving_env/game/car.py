import pygame
from .constants import *


class Car:
    def __init__(self, bump_env):
        self.size = (50, 100)
        self.image = pygame.Surface(
            self.size, pygame.SRCALPHA
        )  # Use SRCALPHA for transparency
        self.color = (0, 0, 255)  # Blue car
        self.bump_env = bump_env

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

        if action == 3 and self.bump_env:
            self.rect.x -= move_speed
            self.rect.x = max(self.rect.x, 0)  # Prevent moving off-screen to the left
            self.turn_angle = 30  # Turn tires left
        if action == 4 and self.bump_env:
            self.rect.x += move_speed
            right_edge = SCREEN_WIDTH - self.rect.width
            self.rect.x = min(
                self.rect.x, right_edge
            )  # Prevent moving off-screen to the right
            self.turn_angle = -30  # Turn tires right
        if action == 1:
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
        elif action == 2:
            self.acceleration = -DECELERATION
            if self.on_grass():
                self.acceleration -= GRASS_FRICTION
            elif self.on_kerbs():
                self.acceleration -= KERB_FRICTION
            elif self.on_road():
                self.acceleration -= ROAD_FRICTION

            if self.velocity == 0:
                self.acceleration = 0
        elif action == 0:
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
        move_speed = 3  # Speed of lateral movement (should be int)
        self.turn_angle = 0  # Reset tire angle
        if keys[pygame.K_LEFT] and self.bump_env:
            self.rect.x -= move_speed
            self.rect.x = max(self.rect.x, 0)  # Prevent moving off-screen to the left
            self.turn_angle = 30  # Turn tires left
        if keys[pygame.K_RIGHT] and self.bump_env:
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
