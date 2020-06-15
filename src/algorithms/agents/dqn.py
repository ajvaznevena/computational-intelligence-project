import random
import os
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.optimizers import Adam
import matplotlib.pyplot as plt

from algorithms.agents.pacman_environment import Environment


class Agent:

    def __init__(self, state_size, action_size, cold_start=False):
        self.weight_backup = "dqn_weight.h5"
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.learning_rate = 0.00025    # old one was 0.001
        self.gamma = 0.95
        self.exploration_rate = 1.0
        self.exploration_min = 0.1      # old one was 0.01
        self.exploration_decay = 0.99998
        self.network = self._build_model()

        self.network.summary()

        if not cold_start:
            if os.path.isfile(self.weight_backup):
                print(f'Loading model from {self.weight_backup}')

                self.load_model()
                self.exploration_rate = self.exploration_min

    def _build_model(self):
        """Builds a neural network for DQN to use."""
        model = Sequential()
        model.add(Conv2D(8, (3, 3), activation='relu', input_shape=(self.state_size[0], self.state_size[1], 1)))
        model.add(Conv2D(16, (3, 3), activation='relu'))
        model.add(Conv2D(32, (4, 4), activation='relu'))    # old one used (3, 3) kernel
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def save_model(self):
        """Saves the model weights to the path set in the object."""
        self.network.save(self.weight_backup)

    def save_model_snapshot(self, episode_id, reward):
        """Saves model weights and encodes the file name parametrized by the episode id and reward."""
        self.network.save(f'episode_{episode_id}_score_{reward}_{self.weight_backup}')

    def load_model(self):
        """Loads the model weights from the path set in the object."""
        self.network.load_weights(self.weight_backup)

    def act(self, state):
        """Acts according to epsilon greedy policy."""
        if np.random.rand() <= self.exploration_rate:
            return random.randrange(self.action_size)

        act_values = self.network.predict(state)
        return np.argmax(act_values[0])

    def act_best_action(self, state):
        """ Act best  according to the learned policy """
        act_values = self.network.predict(self.preprocess_state(state))
        return np.argmax(act_values[0])

    def preprocess_state(self, state):
        return np.expand_dims(state, axis=(0, 3))

    def remember(self, state, action, reward, next_state, done):
        """Saves experience in memory."""
        self.memory.append((state, action, reward, next_state, done))

    def learn(self, sample_batch_size):
        if len(self.memory) < sample_batch_size:
            return

        sample_batch = random.sample(self.memory, sample_batch_size)
        for state, action, reward, next_state, done in sample_batch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.network.predict(next_state)[0])
            target_f = self.network.predict(state)
            target_f[0][action] = target
            self.network.fit(state, target_f, epochs=1, verbose=0)

        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay


class PacmanEnv:
    def __init__(self, cold_start):
        self.sample_batch_size = 32
        self.episodes = 100000
        self.env = Environment()

        self.number_of_snapshots = 30

        self.state_size = self.env.getStateShape()
        self.action_size = self.env.getActionSize()
        self.agent = Agent(self.state_size, self.action_size, cold_start)

    def _preprocess_state(self, state):
        return np.expand_dims(state, axis=(0, 3))

    def load_model(self):
        self.agent.load_model()

    def run_train(self):
        scores = []

        for index_episode in range(self.episodes):
            state = self.env.reset()
            state = self._preprocess_state(state)

            snapshot_step = self.episodes // self.number_of_snapshots

            done = False
            index = 0
            reward = 0
            while not done:
                action = self.agent.act(state)

                next_state, r, done = self.env.step(action)
                next_state = self._preprocess_state(next_state)

                self.agent.remember(state, action, r, next_state, done)
                state = next_state
                index += 1

                reward += r

            print(f'Episode {index_episode + 1}/{self.episodes} Score: {reward} Exploration rate: {self.agent.exploration_rate}')

            scores.append(reward)

            # Save if required
            if index_episode % snapshot_step == 0:
                print(f'Saving model of episode {index_episode}')
                self.agent.save_model_snapshot(index_episode, reward)

            self.agent.learn(self.sample_batch_size)

        self.agent.save_model()

        return scores
