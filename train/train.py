import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback
from x_driving_env.envs import XDrivingEnv

trained = False

env = make_vec_env(
    lambda: XDrivingEnv(bumps_activated=False),
    n_envs=8,
)

if trained:
    saved_model_path = "./models/ppo_driving_last"
    model = PPO.load(saved_model_path, device="cuda:0", env=env)
else:
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=0.0003,
        n_steps=2048,  # Number of steps to run for each environment per update
        batch_size=64,
        n_epochs=10,  # Number of epochs when optimizing the surrogate loss
        gamma=0.99,  # Discount factor
        gae_lambda=0.95,  # Factor for trade-off of bias vs variance for Generalized Advantage Estimator
        ent_coef=0.2,  # Entropy coefficient for exploration
        policy_kwargs=dict(net_arch=dict(pi=[256, 512, 256], vf=[256, 512, 256])),
        device="cuda:0",
    )

checkpoint_callback = CheckpointCallback(
    save_freq=5000, save_path="./models/", name_prefix="ppo_model"
)

model.learn(total_timesteps=int(5e6), callback=checkpoint_callback)

model.save("models/ppo_driving_last")

env.close()
