import gym
from gym import spaces
import numpy as np


class PygletGameEnv(gym.Env):
    def __init__(self):
        super(PygletGameEnv, self).__init__()

        # Define action and observation space
        # Actions: 0 = Left, 1 = Right, 2 = Up, 3 = Down
        self.action_space = spaces.Discrete(4)

        # Observation space: [x_position, y_position]
        self.observation_space = spaces.Box(
            low=0, high=800, shape=(2,), dtype=np.float32
        )

        # Game specific initialization
        self.player_x = 400
        self.player_y = 300
        self.speed = 200

        # Rendering
        self.window = None

    def step(self, action):
        # Implement the logic to update the environment's state
        if action == 0:  # Left
            self.player_x -= self.speed
        elif action == 1:  # Right
            self.player_x += self.speed
        elif action == 2:  # Up
            self.player_y += self.speed
        elif action == 3:  # Down
            self.player_y -= self.speed

        # Calculate reward, done, and info
        reward = 0
        done = False
        info = {}

        # Update the state
        state = np.array([self.player_x, self.player_y])

        return state, reward, done, info

    def reset(self):
        # Reset the state of the environment to an initial state
        self.player_x = 400
        self.player_y = 300
        return np.array([self.player_x, self.player_y])

    def render(self, mode="human"):
        # Implement rendering (optional)
        if self.window is None:
            import pyglet

            self.window = pyglet.window.Window(width=800, height=600)

        self.window.clear()
        # Draw the player as a rectangle (similar to previous example)

    def close(self):
        # Close the environment
        if self.window is not None:
            self.window.close()


# To use the environment
env = PygletGameEnv()
