import pygame
from constants import *


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
