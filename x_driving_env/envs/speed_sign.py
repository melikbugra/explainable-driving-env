import pygame
from .constants import *


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
        text = font.render(str(self.limit * 10), True, (0, 0, 0))
        text_rect = text.get_rect(center=(40, 40))
        self.image.blit(text, text_rect)

    def draw(self, screen, render=False):
        if render:
            if not self.image:
                self.create_image()
            screen.blit(self.image, self.rect.topleft)
