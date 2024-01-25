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
        self.stripes = []

        stripe_height = 100
        stripe_margin = 20
        stripe_group_spacing = stripe_height + stripe_margin

        for i in range(0, SCREEN_HEIGHT, stripe_group_spacing):
            for j in range(3):  # Create 3 stripes in each group
                self.stripes.append(i + (stripe_height + stripe_margin) * j)

    def get_stripe_rects(self):
        self.set_stripes()

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
            for stripe in self.stripes
        ]
