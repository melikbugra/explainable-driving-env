import gym
from gym import spaces
import numpy as np
from ..game.game import Game
import pygame

ROAD_MAX_VELOCITY = 15
SCREEN_WIDTH = 800


class XDrivingEnvBump(gym.Env):
    def __init__(self, bumps_activated=True):
        super().__init__()

        # Define action and observation space

        self.action_space = spaces.MultiDiscrete([3, 3])
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 350, -590], dtype=np.float64),
            high=np.array([10, 10, SCREEN_WIDTH, 450, 410], dtype=np.float64),
            dtype=np.float64,
        )

        self.game = Game(bumps_activated=bumps_activated, bump_env=True)

    def step(self, action):
        # Update game state and get necessary information
        long_action = action[0]
        lat_action = action[1]
        state, reward, done, info = self.game.step(long_action, lat_action)

        car_speed_norm = (state["car_speed"] - self.observation_space.low[0]) / (
            self.observation_space.high[0] - self.observation_space.low[0]
        )
        current_speed_limit_norm = (
            state["current_speed_limit"] - self.observation_space.low[1]
        ) / (self.observation_space.high[1] - self.observation_space.low[1])

        car_x_position_norm = (
            state["car_x_position"] - self.observation_space.low[2]
        ) / (self.observation_space.high[2] - self.observation_space.low[2])

        next_bump_x_position_norm = (
            state["next_bump_x_position"] - self.observation_space.low[3]
        ) / (self.observation_space.high[3] - self.observation_space.low[3])

        next_bump_y_position_norm = (
            state["next_bump_y_position"] - self.observation_space.low[4]
        ) / (self.observation_space.high[4] - self.observation_space.low[4])
        observation = np.array(
            [
                car_speed_norm,
                current_speed_limit_norm,
                car_x_position_norm,
                next_bump_x_position_norm,
                next_bump_y_position_norm,
            ],
            dtype=np.float64,
        )

        return observation, reward, done, info

    def reset(self):
        state = self.game.reset()
        car_speed_norm = (state["car_speed"] - self.observation_space.low[0]) / (
            self.observation_space.high[0] - self.observation_space.low[0]
        )
        current_speed_limit_norm = (
            state["current_speed_limit"] - self.observation_space.low[1]
        ) / (self.observation_space.high[1] - self.observation_space.low[1])

        car_x_position_norm = (
            state["car_x_position"] - self.observation_space.low[2]
        ) / (self.observation_space.high[2] - self.observation_space.low[2])

        next_bump_x_position_norm = (
            state["next_bump_x_position"] - self.observation_space.low[3]
        ) / (self.observation_space.high[3] - self.observation_space.low[3])

        next_bump_y_position_norm = (
            state["next_bump_y_position"] - self.observation_space.low[4]
        ) / (self.observation_space.high[4] - self.observation_space.low[4])
        return np.array(
            [
                car_speed_norm,
                current_speed_limit_norm,
                car_x_position_norm,
                next_bump_x_position_norm,
                next_bump_y_position_norm,
            ],
            dtype=np.float64,
        )

    def render(self, mode="human"):
        if mode == "human":
            self.game.run(render=True)
            pygame.display.flip()

    def close(self):
        pygame.quit()
