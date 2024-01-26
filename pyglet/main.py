import pyglet
from game.game import Game


def main():
    game = Game(bump_env=True)
    game.setup_rendering()
    pyglet.clock.schedule_interval(game.update_game, 1 / 60.0)
    pyglet.app.run()


if __name__ == "__main__":
    main()
