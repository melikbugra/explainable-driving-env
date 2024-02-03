from gymnasium.envs.registration import register

register(
    id="xDriving-v0",
    entry_point="x_driving_env.envs:XDrivingEnv",
)

register(
    id="xDrivingBump-v0",
    entry_point="x_driving_env.envs:XDrivingEnvBump",
)
