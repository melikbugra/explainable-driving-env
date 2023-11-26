import gym
from gym import spaces
import numpy as np
from x_driving_env.envs.game import Game
import pygame

ROAD_MAX_VELOCITY = 15


class XDrivingEnv(gym.Env):
    def __init__(self):
        super().__init__()

        # Define action and observation space
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0]),
            high=np.array([ROAD_MAX_VELOCITY, 15, 800]),
            dtype=np.float32,
        )

        self.game = Game()

    def step(self, action):
        # Update game state and get necessary information
        state, reward, done, info = self.game.step(action)

        # Set observation
        observation = np.array(
            [
                self.game.car.velocity,
                self.game.current_speed_limit,
                self.game.car.rect.centerx,
            ],
            dtype=np.float32,
        )

        return observation, reward, done, info

    def reset(self):
        self.game.reset()
        return np.array(
            [
                self.game.car.velocity,
                self.game.current_speed_limit,
                self.game.car.rect.centerx,
            ],
            dtype=np.float32,
        )

    def render(self, mode="human"):
        if mode == "human":
            self.game.run(render=True)
            pygame.display.flip()

    def close(self):
        pygame.quit()
