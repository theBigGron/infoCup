import torch.nn as nn
import torch.nn.functional as F


class Actor(nn.Module):
    """
    Neuronal Network. Define layer with number of neurons in constructor.
    """
    def __init__(self, state_dim, action_dim):
        super(Actor, self).__init__()
        self.layer_1 = nn.Linear(state_dim, 10)
        self.layer_2 = nn.Linear(10, 10)
        self.layer_3 = nn.Linear(10, 10)
        self.layer_4 = nn.Linear(10, 10)
        self.layer_5 = nn.Linear(10, action_dim)

    def forward(self, state):
        state = F.relu(self.layer_1(state))
        state = F.relu(self.layer_2(state))
        state = F.relu(self.layer_3(state))
        state = F.relu(self.layer_4(state))
        action = self.layer_5(state)

        return action
