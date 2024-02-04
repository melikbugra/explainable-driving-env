import pygame
from .constants import *


class SpeedBump:
    def __init__(self, position, num_rectangles=4):
        self.position = position
        self.num_rectangles = num_rectangles
        self.size = (num_rectangles * (20), 20)
        self.image = None
        self.rect = pygame.Rect(position[0], position[1], self.size[0], self.size[1])
        self.collided = False
        self.passed = False

    def create_image(self):
        # Create the image only when needed
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        x_offset = 0  # Initial x-coordinate offset
        for i in range(self.num_rectangles):
            if i % 2 == 1:
                pygame.draw.rect(
                    self.image,
                    (255, 215, 0),
                    (x_offset, 0, self.size[0] / self.num_rectangles, 20),
                    0,
                    0,
                )
            else:
                pygame.draw.rect(
                    self.image,
                    (0, 0, 0),
                    (x_offset, 0, self.size[0] / self.num_rectangles, 20),
                    0,
                    0,
                )
            x_offset += (
                self.size[0] / self.num_rectangles
            )  # Move x-coordinate to the next rectangle

    def draw(self, screen, render=False):
        if render:
            if not self.image:
                self.create_image()
            screen.blit(self.image, self.rect.topleft)

    def update(self, car_velocity):
        self.position = (
            self.position[0],
            self.position[1] + car_velocity,
        )
        self.rect.y = self.position[1]
