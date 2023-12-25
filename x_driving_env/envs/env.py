import gym
from gym import spaces
import numpy as np
from ..game.game import Game
import pygame

ROAD_MAX_VELOCITY = 15
SCREEN_WIDTH = 800


class XDrivingEnv(gym.Env):
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

        observation = np.array(
            [
                state["car_speed"],
                state["current_speed_limit"],
            ],
            dtype=np.float64,
        )

        return observation, reward, done, info

    def reset(self):
        state = self.game.reset()
        return np.array(
            [
                state["car_speed"],
                state["current_speed_limit"],
            ],
            dtype=np.float64,
        )

    def render(self, mode="human"):
        if mode == "human":
            self.game.run(render=True)
            pygame.display.flip()

    def close(self):
        pygame.quit()
