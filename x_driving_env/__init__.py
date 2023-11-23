from gym.envs.registration import register

register(
    id="xDriving-v1",
    entry_point="x_driving_env.envs:XDrivingEnv",
)
