from algorithms.agents.pacman_environment import Environment

import random
import os
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import matplotlib.pyplot as plt
from algorithms.agents.dqn import PacmanEnv

if __name__ == "__main__":
    pacman = PacmanEnv(True)
    scores = pacman.run_train()
    plt.plot(scores)
    plt.savefig('scores.png')
    plt.show()

# test environment
# if __name__ == "__main__":
#     env = Environment()
#     g = env.reset()
#     # Environment.renderState(g)
#     while True:
#         act = env.sample()
#         # print(act)
#
#         n, rew, done1 = env.step(act)
#         # Environment.renderState(n)
#
#         # print(rew)
#         # print()
#
#         if done1:
#             break
