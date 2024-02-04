import gymnasium
from gymnasium import spaces
import numpy as np
from ..game.game import Game
import pygame

SCREEN_WIDTH = 800
CAR_WIDTH = 50
CAR_MAX_X = SCREEN_WIDTH - CAR_WIDTH


class XDrivingEnvBump(gymnasium.Env):
    def __init__(self, bumps_activated=True):
        super().__init__()

        # Define action and observation space

        self.action_space = spaces.MultiDiscrete([3, 3])
        self.observation_space = spaces.Box(
            low=np.array([0, 3, 3, -1819, 0, 0, -1379], dtype=np.float64),
            high=np.array([10, 10, 10, 480, CAR_MAX_X, 1, 521], dtype=np.float64),
            dtype=np.float64,
        )

        self.game = Game(bumps_activated=bumps_activated, bump_env=True)

    def step(self, action):
        # Update game state and get necessary information
        long_action = action[0]
        lat_action = action[1]
        state, reward, done, info = self.game.step(long_action, lat_action)
        terminated = done
        truncated = False

        observation = np.array(
            [
                state["car_speed"],
                state["current_speed_limit"],
                state["next_speed_limit"],
                state["next_sign_y_position"],
                state["car_x_position"],
                state["next_bump_x_position"],
                state["next_bump_y_position"],
            ],
            dtype=np.float64,
        )

        return observation, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        state = self.game.reset()

        info = {}

        return (
            np.array(
                [
                    state["car_speed"],
                    state["current_speed_limit"],
                    state["next_speed_limit"],
                    state["next_sign_y_position"],
                    state["car_x_position"],
                    state["next_bump_x_position"],
                    state["next_bump_y_position"],
                ],
                dtype=np.float64,
            ),
            info,
        )

    def render(self, mode="human"):
        if mode == "human":
            self.game.run(render=True)
            pygame.display.flip()

    def close(self):
        pygame.quit()
