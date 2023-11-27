import gym
from gym import spaces
import numpy as np
from .game import Game
import pygame

ROAD_MAX_VELOCITY = 15
SCREEN_WIDTH = 800


class XDrivingEnv(gym.Env):
    def __init__(self):
        super().__init__()

        # Define action and observation space
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 350, -590]),
            high=np.array([SCREEN_WIDTH, 15, 450, 410]),
            dtype=np.float32,
        )

        self.game = Game()

    def step(self, action):
        # Update game state and get necessary information
        state, reward, done, info = self.game.step(action)

        # Set observation
        observation = np.array(
            [
                state["car_x_position"],
                state["current_speed_limit"],
                state["next_bump_x_position"],
                state["next_bump_y_position"],
            ],
            dtype=np.float32,
        )

        return observation, reward, done, info

    def reset(self):
        state = self.game.reset()
        return np.array(
            [
                state["car_x_position"],
                state["current_speed_limit"],
                state["next_bump_x_position"],
                state["next_bump_y_position"],
            ],
            dtype=np.float32,
        )

    def render(self, mode="human"):
        if mode == "human":
            self.game.run(render=True)
            pygame.display.flip()

    def close(self):
        pygame.quit()
