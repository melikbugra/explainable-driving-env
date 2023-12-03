import gym
from gym import spaces
import numpy as np
from .game import Game
import pygame

ROAD_MAX_VELOCITY = 15
SCREEN_WIDTH = 800


class XDrivingEnv(gym.Env):
    def __init__(self, bumps_activated=False):
        super().__init__()
        self.bumps_activated = bumps_activated
        # Define action and observation space
        if self.bumps_activated:
            self.action_space = spaces.Discrete(5)
            self.observation_space = spaces.Box(
                low=np.array([0, 0, 350, -590], dtype=np.float64),
                high=np.array([SCREEN_WIDTH, 10, 450, 410], dtype=np.float64),
                dtype=np.float64,
            )
        else:
            self.action_space = spaces.Discrete(3)
            self.observation_space = spaces.Box(
                low=np.array([0, 0], dtype=np.float64),
                high=np.array([10, 10], dtype=np.float64),
                dtype=np.float64,
            )

        self.game = Game(bumps_activated)

    def step(self, action):
        # Update game state and get necessary information
        state, reward, done, info = self.game.step(action)

        # Set observation
        if self.bumps_activated:
            observation = np.array(
                [
                    state["car_x_position"],
                    state["current_speed_limit"],
                    state["next_bump_x_position"],
                    state["next_bump_y_position"],
                ],
                dtype=np.float64,
            )
        else:
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
        if self.bumps_activated:
            return np.array(
                [
                    state["car_x_position"],
                    state["current_speed_limit"],
                    state["next_bump_x_position"],
                    state["next_bump_y_position"],
                ],
                dtype=np.float64,
            )
        else:
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
