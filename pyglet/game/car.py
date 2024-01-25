from pyglet.graphics import Batch
from pyglet.shapes import Rectangle, Line

from .constants import *


class Car:
    def __init__(self):
        self.width = 50
        self.height = 100
        self.color = (0, 0, 255)
        self.position_x = SCREEN_WIDTH / 2 - self.width / 2
        self.position_y = SCREEN_HEIGHT / 10
        self.window_color = (135, 206, 235)

        self.batch = Batch()
        # We put body here because we will use its position for collision
        self.body_rect = self.get_body_rect()

    def draw(self):
        # We put these here because they are only for visualization purposes
        window_rects = self.get_window_rects()
        bodywork_line_rect = self.get_bodywork_line()
        tire_rects = self.get_tire_rects()

        self.batch.draw()

    def get_body_rect(self):
        return Rectangle(
            x=self.position_x,
            y=self.position_y,
            width=self.width,
            height=self.height,
            color=self.color,
            batch=self.batch,
        )

    def get_window_rects(self):
        return (
            Rectangle(
                x=self.position_x + 10,
                y=self.position_y + self.height - 30,
                width=30,
                height=20,
                color=self.window_color,
                batch=self.batch,
            ),
            Rectangle(
                x=self.position_x + 10,
                y=self.position_y + 10,
                width=30,
                height=20,
                color=self.window_color,
                batch=self.batch,
            ),
        )

    def get_bodywork_line(self):
        return Line(
            x=self.position_x + 10,
            y=self.position_y + self.height - 40,
            x2=self.position_x + 40,
            y2=self.position_y + self.height - 40,
            color=(0, 0, 0),
            batch=self.batch,
        )

    def get_tire_rects(self):
        tire_width = 8
        tire_height = 20

        tires = []

        front_left_tire = Rectangle(
            x=self.position_x - tire_width / 3,
            y=self.position_y + self.height - 26,
            width=tire_width,
            height=tire_height,
            color=(0, 0, 0),
            batch=self.batch,
        )
        tires.append(front_left_tire)

        front_right_tire = Rectangle(
            x=self.position_x + self.width - tire_width * 2 / 3,
            y=self.position_y + self.height - 26,
            width=tire_width,
            height=tire_height,
            color=(0, 0, 0),
            batch=self.batch,
        )
        tires.append(front_right_tire)

        rear_left_tire = Rectangle(
            x=self.position_x - tire_width / 3,
            y=self.position_y + 6,
            width=tire_width,
            height=tire_height,
            color=(0, 0, 0),
            batch=self.batch,
        )
        tires.append(rear_left_tire)

        rear_right_tire = Rectangle(
            x=self.position_x + self.width - tire_width * 2 / 3,
            y=self.position_y + 6,
            width=tire_width,
            height=tire_height,
            color=(0, 0, 0),
            batch=self.batch,
        )
        tires.append(rear_right_tire)

        return tires
