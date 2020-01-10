import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


# noinspection DuplicatedCode
class Critic(nn.Module):

    """
    Evaluates action, state combination

    Evaluates the action and state combination for better predictions.
    """

    def __init__(self, state_dim: int, action_dim: int):
        super(Critic, self).__init__()
        # Critic 1
        self.layer_1 = nn.Linear(state_dim + action_dim, 10)
        self.layer_2 = nn.Linear(10, 10)
        self.layer_3 = nn.Linear(10, 10)
        self.layer_4 = nn.Linear(10, 1)
        # Critic 2
        self.layer_5 = nn.Linear(state_dim + action_dim, 10)
        self.layer_6 = nn.Linear(10, 10)
        self.layer_7 = nn.Linear(10, 10)
        self.layer_8 = nn.Linear(10, 1)

    def forward(self, state: np.array, action: np.array):
        """
        Returns 2 Q-Values from different critics.

        :param state: Current State
        :param action: Current Actions
        :return:
        """
        action_state = torch.cat([state, action], 1)
        # Critic 1
        action_state_1 = F.relu(self.layer_1(action_state))
        action_state_1 = F.relu(self.layer_2(action_state_1))
        action_state_1 = F.relu(self.layer_3(action_state_1))
        q_value_c1 = self.layer_4(action_state_1)
        # Critic 2
        action_state_2 = F.relu(self.layer_5(action_state))
        action_state_2 = F.relu(self.layer_6(action_state_2))
        action_state_2 = F.relu(self.layer_7(action_state_2))
        q_value_c2 = self.layer_8(action_state_2)
        # Return both Q-Values at once
        return q_value_c1, q_value_c2

    def calc_q1(self, state: np.array, action: np.array) -> np.array:
        """
        Returns Q-Values from first critic.

        This is used for gradient descent for updating the weights of the actor model.

        :param state: Current State
        :param action: Current Actions
        :return:
        """
        action_state = torch.cat([state, action], 1)
        # Critic 1
        action_state_1 = F.relu(self.layer_1(action_state))
        action_state_1 = F.relu(self.layer_2(action_state_1))
        action_state_1 = F.relu(self.layer_3(action_state_1))
        q_value = self.layer_4(action_state_1)
        return q_value
