import gymnasium
from gymnasium import spaces
import numpy as np
from ..game.game import Game
import pygame

ROAD_MAX_VELOCITY = 15
SCREEN_WIDTH = 800


class XDrivingEnv(gymnasium.Env):
    def __init__(self):
        super().__init__()
        # Define action and observation space

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(
            low=np.array([0, 0], dtype=np.float64),
            high=np.array([10, 10], dtype=np.float64),
            dtype=np.float64,
        )

        self.game = Game()

    def step(self, action):
        # Update game state and get necessary information

        state, reward, done, info = self.game.step(action)
        terminated = done
        truncated = False

        observation = np.array(
            [
                state["car_speed"],
                state["current_speed_limit"],
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
