from pyglet.graphics import Batch
from pyglet.shapes import Rectangle, Line

from .constants import *


class Road:
    def __init__(self):
        self.batch = Batch()

        self.asphalt_rect = self.get_asphalt_rect()
        self.left_grass_rect = self.get_left_grass_rect()
        self.right_grass_rect = self.get_right_grass_rect()

    def draw(self):
        stripe_rects = self.get_stripe_rects()
        kerb_rects = self.get_kerb_rects()

        self.batch.draw()

    def get_asphalt_rect(self):
        return Rectangle(
            x=GRASS_WIDTH + KERB_WIDTH,
            y=0,
            width=ROAD_WIDTH,
            height=SCREEN_HEIGHT,
            color=ASPHALT_COLOR,
            batch=self.batch,
        )

    def get_left_grass_rect(self):
        return Rectangle(
            x=0,
            y=0,
            width=GRASS_WIDTH,
            height=SCREEN_HEIGHT,
            color=GRASS_COLOR,
            batch=self.batch,
        )

    def get_right_grass_rect(self):
        return Rectangle(
            x=SCREEN_WIDTH - GRASS_WIDTH,
            y=0,
            width=GRASS_WIDTH,
            height=SCREEN_HEIGHT,
            color=GRASS_COLOR,
            batch=self.batch,
        )

    def set_stripes(self):
        stripes = []

        stripe_height = 100
        stripe_margin = 20
        stripe_group_spacing = stripe_height + stripe_margin

        for i in range(0, SCREEN_HEIGHT, stripe_group_spacing):
            for j in range(3):  # Create 3 stripes in each group
                stripes.append(i + (stripe_height + stripe_margin) * j)

        return stripes

    def get_stripe_rects(self):
        stripes = self.set_stripes()

        stripe_width = 10
        stripe_height = 100
        return [
            Rectangle(
                x=SCREEN_WIDTH / 2 - stripe_width / 2,
                y=stripe,
                width=stripe_width,
                height=stripe_height,
                batch=self.batch,
            )
            for stripe in stripes
        ]

    def set_kerbs(self):
        self.kerb_offset = 0
        kerbs = []
        for y in range(0, SCREEN_HEIGHT // KERB_WIDTH):
            kerbs.append(KERB_COLORS[y % 2])  # Alternating red and white
        return kerbs

    def get_kerb_rects(self):
        kerbs = self.set_kerbs()

        kerb_rects = []

        for y in range(-KERB_HEIGHT, SCREEN_HEIGHT, KERB_HEIGHT):
            kerb_color = kerbs[
                (y // KERB_HEIGHT + int(self.kerb_offset) // KERB_HEIGHT) % len(kerbs)
            ]

            left_kerb = Rectangle(
                x=GRASS_WIDTH,
                y=y + int(self.kerb_offset) % KERB_HEIGHT,
                width=KERB_WIDTH,
                height=KERB_HEIGHT,
                color=kerb_color,
                batch=self.batch,
            )
            right_kerb = Rectangle(
                x=GRASS_WIDTH + ROAD_WIDTH + KERB_WIDTH,
                y=y + int(self.kerb_offset) % KERB_HEIGHT,
                width=KERB_WIDTH,
                height=KERB_HEIGHT,
                color=kerb_color,
                batch=self.batch,
            )
            kerb_rects.append(left_kerb)
            kerb_rects.append(right_kerb)

        return kerb_rects
