import pyglet
from pyglet.window import key, Window

from .constants import *
from .car import Car
from .road import Road


class Game:
    def __init__(self, render=False):
        # Initialize game...
        self.window: Window = None
        if render:
            self.window = Window(
                width=SCREEN_WIDTH, height=SCREEN_HEIGHT, caption="Pyglet Game"
            )
            self.window.push_handlers(self)

        self.car = Car()
        self.road = Road()

    def on_draw(self):
        self.window.clear()

        self.road.draw()
        self.car.draw()


if __name__ == "__main__":
    game = Game(True)
    pyglet.app.run()
