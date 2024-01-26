import pyglet
from pyglet.window import key, Window

from .constants import *
from .car import Car
from .road import Road


class Game:
    def __init__(self, bumps_activated=False, bump_env=False):
        self.car = Car(self, bump_env=bump_env)
        self.road = Road()

    def setup_rendering(self):
        self.window = Window(
            width=SCREEN_WIDTH, height=SCREEN_HEIGHT, caption="Explainable Driving Env"
        )
        self.key_handler = key.KeyStateHandler()
        self.keys = {}
        self.window.push_handlers(self)
        self.window.push_handlers(self.key_handler)

    def on_draw(self):
        self.window.clear()

        self.road.draw()
        self.car.draw()

    def update_game(self, dt):
        self.car.update()

    def on_key_press(self, symbol, modifiers):
        self.keys[symbol] = True

    def on_key_release(self, symbol, modifiers):
        del self.keys[symbol]

    def is_key_pressed(self, symbol):
        return self.keys.get(symbol, False)
