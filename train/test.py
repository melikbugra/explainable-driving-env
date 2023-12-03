from stable_baselines3 import PPO
from x_driving_env.envs import XDrivingEnv

model = PPO.load("models/ppo_driving_last")
env = XDrivingEnv(bumps_activated=False)

num_episodes = 10
for episode in range(num_episodes):
    obs = env.reset()
    done = False
    total_reward = 0

    while not done:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        env.render()

    print(f"Episode: {episode + 1}, Total Reward: {total_reward}")

env.close()
