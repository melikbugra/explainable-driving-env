import gymnasium
from gymnasium import spaces
import numpy as np
from ..game.game import Game
import pygame

ROAD_MAX_VELOCITY = 15
SCREEN_WIDTH = 800


class XDrivingEnv(gymnasium.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None):
        super().__init__()
        # Define action and observation space

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(
            low=np.array([0, 3, 3, -1819], dtype=np.float64),
            high=np.array([10, 10, 10, 480], dtype=np.float64),
            dtype=np.float64,
        )

        self.game = Game()
        self.render_mode = render_mode

    def step(self, action):
        # Update game state and get necessary information

        state, reward, done, info = self.game.step(action)
        terminated = done
        truncated = False

        observation = np.array(
            [
                state["car_speed"],
                state["current_speed_limit"],
                state["next_speed_limit"],
                state["next_sign_y_position"],
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
