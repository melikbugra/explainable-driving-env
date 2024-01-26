import x_driving_env
import gym

env = gym.make("xDriving-v0")

done = False

while True:
    state = env.reset()
    while not done:
        action = [0, 0]
        reward, state, done, info = env.step(action)
        # print(reward)
    print(done)
    done = False
