from pyglet.graphics import Batch
from pyglet.shapes import Rectangle, Line
from pyglet.window import key

from .constants import *


class Car:
    def __init__(self, game_instance, bump_env):
        self.game = game_instance
        self.bump_env = bump_env

        self.width = 50
        self.height = 100
        self.color = (0, 0, 255)
        self.position_x = SCREEN_WIDTH / 2 - self.width / 2
        self.position_y = SCREEN_HEIGHT / 10
        self.window_color = (135, 206, 235)

        self.velocity = MIN_SPEED
        self.acceleration = 0
        self.turn_angle = 0

        self.batch = Batch()

    def get_pressed_keys(self):
        if self.game.rendering_set:
            return self.game.keys

    def is_key_pressed(self, symbol):
        if self.game.rendering_set:
            return self.get_pressed_keys().get(symbol, False)

    def draw(self):
        body_rect = self.get_body_rect()
        window_rects = self.get_window_rects()
        bodywork_line_rect = self.get_bodywork_line()
        tire_rects = self.get_tire_rects()

        self.batch.draw()

    def update(self, long_action=None, lat_action=None):
        if long_action is not None:
            # Handle actions programmatically
            self.handle_action(long_action, lat_action)
            pass
        else:
            # Handle keyboard input
            self.handle_keyboard_input()

    def handle_action(self, long_action, lat_action=None):
        move_speed = 2  # Speed of lateral movement (should be int)
        self.turn_angle = 0  # Reset tire angle

        if lat_action == 1 and self.bump_env:
            self.position_x -= move_speed
            self.position_x = max(
                self.position_x, 0
            )  # Prevent moving off-screen to the left
            self.turn_angle = -30  # Turn tires left
        if lat_action == 2 and self.bump_env:
            self.position_x += move_speed
            right_edge = SCREEN_WIDTH - self.width
            self.position_x = min(
                self.position_x, right_edge
            )  # Prevent moving off-screen to the right
            self.turn_angle = 30  # Turn tires right
        if long_action == 1:
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
        elif long_action == 2:
            self.acceleration = -DECELERATION
            if self.on_grass():
                self.acceleration -= GRASS_FRICTION
            elif self.on_kerbs():
                self.acceleration -= KERB_FRICTION
            elif self.on_road():
                self.acceleration -= ROAD_FRICTION

            if self.velocity == MIN_SPEED:
                self.acceleration = 0
        elif long_action == 0:
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

            if self.velocity == MIN_SPEED:
                self.acceleration = 0

        # Update velocity based on acceleration
        self.velocity += self.acceleration
        self.velocity = max(MIN_SPEED, min(self.velocity, ROAD_MAX_VELOCITY))

    def handle_keyboard_input(self):
        keys = self.get_pressed_keys()
        move_speed = 3  # Speed of lateral movement (should be int)
        self.turn_angle = 0  # Reset tire angle

        if self.is_key_pressed(key.LEFT) and self.bump_env:
            self.position_x -= move_speed
            self.position_x = max(
                self.position_x, 0
            )  # Prevent moving off-screen to the left
            self.turn_angle = -30  # Turn tires left

        if self.is_key_pressed(key.RIGHT) and self.bump_env:
            self.position_x += move_speed
            right_edge = SCREEN_WIDTH - self.width
            self.position_x = min(
                self.position_x, right_edge
            )  # Prevent moving off-screen to the right
            self.turn_angle = 30  # Turn tires right

        if self.is_key_pressed(key.UP):
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

        elif self.is_key_pressed(key.DOWN):
            self.acceleration = -DECELERATION
            if self.on_grass():
                self.acceleration -= GRASS_FRICTION
            elif self.on_kerbs():
                self.acceleration -= KERB_FRICTION
            elif self.on_road():
                self.acceleration -= ROAD_FRICTION

            if self.velocity == MIN_SPEED:
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

            if self.velocity == MIN_SPEED:
                self.acceleration = 0

        # Update velocity based on acceleration
        self.velocity += self.acceleration
        self.velocity = max(MIN_SPEED, min(self.velocity, ROAD_MAX_VELOCITY))

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
            (self.position_x, self.position_y + self.height),
            (self.position_x + self.width, self.position_y + self.height),
            (self.position_x, self.position_y),
            (self.position_x + self.width, self.position_y),
        ]

    def is_point_on_road(self, point):
        x, _ = point
        return GRASS_WIDTH + KERB_WIDTH <= x <= GRASS_WIDTH + KERB_WIDTH + ROAD_WIDTH

    def is_point_on_kerbs(self, point):
        x, _ = point
        return (GRASS_WIDTH < x < GRASS_WIDTH + KERB_WIDTH) or (
            GRASS_WIDTH + KERB_WIDTH + ROAD_WIDTH
            < x
            < GRASS_WIDTH + KERB_WIDTH * 2 + ROAD_WIDTH
        )

    def is_point_on_grass(self, point):
        x, _ = point
        return x <= GRASS_WIDTH or x >= GRASS_WIDTH + KERB_WIDTH * 2 + ROAD_WIDTH

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
        front_left_tire.x += tire_width / 2  # to place better after setting anchor
        front_left_tire.y += tire_height / 2  # to place better after setting anchor
        front_left_tire.anchor_position = (
            tire_width / 2,
            tire_height / 2,
        )
        front_left_tire.rotation = self.turn_angle

        tires.append(front_left_tire)

        front_right_tire = Rectangle(
            x=self.position_x + self.width - tire_width * 2 / 3,
            y=self.position_y + self.height - 26,
            width=tire_width,
            height=tire_height,
            color=(0, 0, 0),
            batch=self.batch,
        )
        front_right_tire.x += tire_width / 2  # to place better after setting anchor
        front_right_tire.y += tire_height / 2  # to place better after setting anchor
        front_right_tire.anchor_position = (
            tire_width / 2,
            tire_height / 2,
        )
        front_right_tire.rotation = self.turn_angle

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
