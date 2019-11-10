from collections import deque
import random

import numpy as np
from torch import cuda
from torch import nn, tensor, squeeze, argmax, add, mul, optim

from agents.dqn_agent import DQNAgent
from models.torch_model import TorchModel


class TorchDQNAgent(DQNAgent):
    def __init__(self, state_size, action_size, gym_env, memory=deque(maxlen=1000000), gamma=0.99, batch_size=34,
                 epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.996, learning_rate=0.001, model=None):
        super().__init__(state_size, action_size, gym_env, memory, gamma, batch_size, epsilon, epsilon_min,
                         epsilon_decay, learning_rate, model)

    def _build_model(self):
        model = nn.Sequential(nn.Linear(self.state_size, 150),
                              nn.ReLU(),
                              nn.Linear(150, 120),
                              nn.ReLU(),
                              nn.Linear(120, self.action_size),
                              )
        # _model = Sequential()
        # _model.add(Dense(150, input_dim=self.state_size, activation='relu'))
        # _model.add(Dense(120, activation='relu'))
        # _model.add(Dense(self.action_size, activation='linear'))
        # _model.compile(loss='mse',
        #               optimizer=Adam(lr=self.learning_rate))

        return TorchModel(model, lr=0.001)

    def _replay(self, batch_size=64):
        if len(self.memory) < batch_size:
            return

        # minibatch = random.sample(self.memory, batch_size)
        # states = tensor([i[0] for i in minibatch], requires_grad=True).to("cuda")
        # actions = tensor([i[1] for i in minibatch], requires_grad=True).to("cuda")
        # rewards = tensor([i[2] for i in minibatch], requires_grad=True).to("cuda")
        # next_states = tensor([i[3] for i in minibatch], requires_grad=True).to("cuda")
        # dones = tensor([i[4] for i in minibatch], requires_grad=True).to("cuda")

        # states = squeeze(states)
        # next_states = squeeze(next_states)

        # targets = add(rewards, mul(self.gamma, mul((argmax(self._model.predict(next_states), dim=1)) * (1 - dones))))
        # targets_full = self._model.predict(states)
        # ind = np.array([i for i in range(batch_size)])
        # targets_full[[ind], [actions]] = targets

        if len(self.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma * (np.amax(self._model.predict(next_states), axis=1)) * (1 - dones)
        targets_full = self._model.predict(states)
        ind = np.array([i for i in range(batch_size)])
        targets_full[[ind], [actions]] = targets

        # Convert to ndarrays to tensors
        states = states
        targets_full = targets_full

        self._model.fit(states, targets_full)