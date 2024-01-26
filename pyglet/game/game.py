import random
from pyglet.window import key, Window

from .constants import *
from .car import Car
from .road import Road
from .speed_sign import SpeedSign


class Game:
    def __init__(self, bumps_activated=False, bump_env=False):
        self.bumps_activated = bumps_activated
        self.bump_env = bump_env
        self.initial_state()
        self.rendering_set = False

    def setup_rendering(self):
        self.window = Window(
            width=SCREEN_WIDTH, height=SCREEN_HEIGHT, caption="Explainable Driving Env"
        )
        self.key_handler = key.KeyStateHandler()
        self.keys = {}
        self.window.push_handlers(self)
        self.window.push_handlers(self.key_handler)
        self.rendering_set = True

    def initial_state(self):
        self.time = 0  # Record the start time
        self.car = Car(self, bump_env=self.bump_env)
        self.road = Road()
        self.distance_travelled = 0
        self.game_over = False
        self.reward = 0
        self.score = 0
        self.speed_signs: list[SpeedSign] = []
        self.speed_bumps = []
        self.current_speed_limit = 10
        self.next_bump_x_position = 0
        self.next_bump_y_position = 0
        self.current_speed_sign_image = None
        self.generate_speed_signs()
        # if self.bumps_activated:
        #     self.generate_speed_bumps()

    def generate_speed_signs(self):
        distances = range(0, END_POINT_DISTANCE + 1, 5000)
        for d in distances:
            limit = random.choice([3, 5, 7, 10])
            position = (SCREEN_WIDTH // 2 + ROAD_WIDTH - 20, d + SCREEN_HEIGHT * 2 / 3)
            self.speed_signs.append(SpeedSign(limit, position))

    def on_draw(self):
        self.window.clear()

        self.road.draw()
        self.car.draw()
        for speed_sign in self.speed_signs:
            speed_sign.draw()

    def update_game(self, dt):
        self.car.update()

    def on_key_press(self, symbol, modifiers):
        self.keys[symbol] = True

    def on_key_release(self, symbol, modifiers):
        del self.keys[symbol]

    def is_key_pressed(self, symbol):
        return self.keys.get(symbol, False)
