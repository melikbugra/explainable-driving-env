from x_driving_env.game.game import Game
import cProfile

import x_driving_env
import gym


def run_random():
    game = Game()
    state = game.reset()
    done = False
    while not done:
        state, reward, done, info = game.step([0, 0])


def run_with_env():
    env = gym.make("xDriving-v0")
    state = env.reset()
    done = False
    while not done:
        state, reward, done, info = env.step([0, 0])


if __name__ == "__main__":
    game = Game(bump_env=False, bumps_activated=False)
    game.setup_rendering()
    # profile = cProfile.Profile()
    # profile.enable()
    # run_random()
    # profile.disable()

    # profile.print_stats(sort="time")
    # cProfile.run("run_with_env()", sort=)

    game.run_game()
