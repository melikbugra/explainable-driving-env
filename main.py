from x_driving_env.game.game import Game
import cProfile

if __name__ == "__main__":
    game = Game(bumps_activated=True, bump_env=True)
    game.setup_rendering()
    # cProfile.run("game.run_game()")

    game.run_game()
