from x_driving_env.envs.game import Game
import cProfile

if __name__ == "__main__":
    game = Game(bumps_activated=False)
    # cProfile.run("game.run_game()")

    game.run_game()
