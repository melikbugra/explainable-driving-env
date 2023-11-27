import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback
from x_driving_env.envs import XDrivingEnv

trained = True

env = make_vec_env(XDrivingEnv, n_envs=8)

if trained:
    saved_model_path = "./models/ppo_model_960000_steps"
    model = PPO.load(saved_model_path, env=env)
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
        ent_coef=0.0,  # Entropy coefficient for exploration
        policy_kwargs=dict(net_arch=dict(pi=[256, 256], vf=[256, 256])),
    )

checkpoint_callback = CheckpointCallback(
    save_freq=10000, save_path="./models/", name_prefix="ppo_model"
)

model.learn(total_timesteps=int(1e6), callback=checkpoint_callback)

model.save("ppo_driving")

env.close()
