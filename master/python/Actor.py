import torch
import torch.nn as nn
import torch.nn.functional as F


class Actor(nn.Module):
    """
    Actor for Neuronal Network. Define layer with number of neurons in constructor.
    """
    def __init__(self, state_dim, action_dim, max_action):
        super(Actor, self).__init__()
        self.layer_1 = nn.Linear(state_dim, 200)
        self.layer_2 = nn.Linear(200, 300)
        self.layer_3 = nn.Linear(300, 100)
        self.layer_4 = nn.Linear(100, 30)
        self.layer_5 = nn.Linear(30, 50)
        self.layer_6 = nn.Linear(50, action_dim)
        self.max_action = max_action

    def forward(self, state):
        state = F.relu(self.layer_1(state))
        state = F.relu(self.layer_2(state))
        state = F.relu(self.layer_3(state))
        state = F.relu(self.layer_4(state))
        state = F.relu(self.layer_5(state))
        action = torch.tanh(self.layer_6(state))

        return action
