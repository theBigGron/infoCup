import io
import os
import tarfile
from typing import List, Tuple

import numpy as np
import torch
import torch.nn.functional as F

from common.d3t_agent.Actor import Actor
from common.d3t_agent.Critic import Critic

from common.d3t_agent.ReplayMemory import ReplayBuffer

# Selecting the device (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class TD3:

    def __init__(self, state_dim, action_dim):
        """
        Crates a twin delayed deep deterministic policy gradient actor.


        :param state_dim: Number of data points the networks uses as input.
        :param action_dim: Number of actions the nerwork can choose from.
        :param max_action: Maximum activation possible for a datapoint. Used to
                           clip activation after adding noise to state_dim data.
        """
        # Loading actor and critic target
        self.actor = Actor(state_dim, action_dim).to(device)
        self.actor_target = Actor(state_dim, action_dim).to(device)
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters())
        # Loading critic and critic target
        self.critic = Critic(state_dim, action_dim).to(device)
        self.critic_target = Critic(state_dim, action_dim).to(device)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters())

    def select_action(self, state: np.array):
        """
        Casts state into tensor.
        Calculates activations from state_tensor.

        :param state: Numpy representation of state.
        :return: Neural network activations for action.
        """
        state = torch.Tensor(state.reshape(1, -1)).to(device)
        res = self.actor(state).cpu().data.numpy().flatten()
        return res

    def train(self,
              replay_buffer: ReplayBuffer,
              iterations: int,
              batch_size: int = 1000,
              discount: float = 0.99,
              tau: float = 0.05,
              policy_freq: int = 3):
        """
        Trains the neural network on given data. For multiple iterations.

        :param replay_buffer: Buffer that holds all actions and their results plus rewards.
        :param iterations: How many times we should train on the data.
        :param batch_size: Batch size.
        :param discount: Discount of future q Values.
        :param tau: Discount factor for polyak averaging.
        :param policy_freq: Number of steps taken before update ist performed.
        :return:
        """

        for it in range(iterations):

            # Step 4: We sample a batch of transitions (s, s’, a, r) from the memory
            batch_states, batch_next_states, batch_actions, batch_rewards = replay_buffer.sample(
                batch_size=batch_size, )
            state = torch.Tensor(batch_states).to(device)
            next_state = torch.Tensor(batch_next_states).to(device)
            action = torch.Tensor(batch_actions).to(device)
            reward = torch.Tensor(batch_rewards).to(device)

            # Step 5: From the next state s’, the Actor target plays the next action a’
            next_action = self.actor_target(next_state)

            # Step 6: We add Gaussian noise to this next action a’ and we clamp it in a range of values supported by
            # the environment
            noise = torch.Tensor(np.random.normal(0, 0.05, 12)).to(device)
            next_action = (next_action+noise).clamp(-1, 1)

            # Step 7: The two Critic targets take each the couple (s’, a’) as input and return two Q-values Qt1(s’,
            # a’) and Qt2(s’,a’) as outputs
            target_Q1, target_Q2 = self.critic_target(next_state, next_action)

            # Step 8: We keep the minimum of these two Q-values: min(Qt1, Qt2)
            target_Q = torch.min(target_Q1, target_Q2)

            # Step 9: We get the final target of the two Critic models, which is: Qt = r + γ * min(Qt1, Qt2),
            # where γ is the discount factor
            target_Q = reward + ((1 - 0) * discount * target_Q).detach()

            # Step 10: The two Critic models take each the couple (s, a) as input and return two Q-values Q1(s,
            # a) and Q2(s,a) as outputs
            current_Q1, current_Q2 = self.critic(state, action)

            # Step 11: We compute the loss coming from the two Critic models: Critic Loss = MSE_Loss(Q1(s,a),
            # Qt) + MSE_Loss(Q2(s,a), Qt)
            critic_loss = F.mse_loss(current_Q1, target_Q) + F.mse_loss(current_Q2, target_Q)

            # Step 12: We backpropagate this Critic loss and update the parameters of the two Critic models with a
            # SGD optimizer
            self.critic_optimizer.zero_grad()
            critic_loss.backward()
            self.critic_optimizer.step()

            # Step 13: Once every two iterations, we update our Actor model by performing gradient ascent on the
            # output of the first Critic model
            if it % policy_freq == 0:
                actor_loss = -self.critic.calc_q1(state, self.actor(state)).mean()
                self.actor_optimizer.zero_grad()
                actor_loss.backward()
                self.actor_optimizer.step()

                # Step 14: Still once every two iterations, we update the weights of the Actor target by polyak
                # averaging
                for param, target_param in zip(self.actor.parameters(), self.actor_target.parameters()):
                    target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)

                # Step 15: Still once every two iterations, we update the weights of the Critic target by polyak
                # averaging
                for param, target_param in zip(self.critic.parameters(), self.critic_target.parameters()):
                    target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)

    # Making a save method to save a trained model
    def save(self, dir_):
        """
        Save model of given type.

        Save actual model from neuronal Network in with itetation counter
        also overrides current newest model.

        :param: Type of Agent: Disease or City
        :return: None
        """
        for directory in ["max", dir_]:
            if not os.path.exists(f'{directory}'):
                os.makedirs(f'{directory}')
            actor_path = f'{directory}/actor.pth.tar'
            torch.save({'state_dict': self.actor.state_dict()}, actor_path)

            actor_target_path = f'{directory}/actor_target.pth.tar'
            torch.save({'state_dict': self.actor_target.state_dict()}, actor_target_path)

            critic_path = f'{directory}/critic.pth.tar'
            torch.save({'state_dict': self.critic.state_dict()}, critic_path)

            critic_target_path = f'{directory}/critic_target.pth.tar'
            torch.save({'state_dict': self.critic_target.state_dict()}, critic_target_path)

    def get_models(self, ) -> List[Tuple[str, str, bytes]]:
        """
        Retrieves pth.tar representation for all models of specified agent type.

        :return: list containing a tuple of agent_name, pth.tar as binary
                 (City, _agent_target,City_agent_target.pth.tar as binary)
        """
        model_list = []
        types_ = ["actor", "actor_target", "critic", "critic_target"]
        for ctr, model in enumerate([self.actor, self.actor_target, self.critic, self.critic_target]):
            buffer = io.BytesIO()
            torch.save({'state_dict': model.state_dict()}, buffer)
            data = buffer.getvalue()
            model_list.append((types_[ctr], data))
        return model_list

    # Making a load method to load a pre-trained model
    def load(self, directory=None) -> None:
        """
        Load stored model weights from pth.tar files laying in given directory.

        :param directory: Directory to load from.
        :return: None
        """
        if directory is not None:
            self.load_from_dir(directory)
        else:
            if os.path.exists(f'/max'):
                self.load_from_dir("max")
            else:
                print("path does not exist")
                raise FileNotFoundError

    def load_bin(self, models: List[Tuple[tarfile.TarFile, str]]) -> None:
        """
        Loads all 4 models from a list of models.
        :param models: List of models as tarFile loaded to a binary buffer.
        :return: None
        """
        for model in models:
            checkpoint = torch.load(model[0])["state_dict"]
            if "actor_target" in model[1]:
                self.actor_target.load_state_dict(checkpoint)
            elif "actor" in model[1]:
                self.actor.load_state_dict(checkpoint)
            elif "critic_target" in model[1]:
                self.critic_target.load_state_dict(checkpoint)
            elif "critic" in model[1]:
                self.critic.load_state_dict(checkpoint)

    def load_from_dir(self, directory: str) -> None:
        """ Loads model from dir
        Loads stored weights of given agent type from Directory.

        :param directory: Directory to load model from.
        :return: None
        """
        checkpoint = torch.load(f'{directory}/actor.pth.tar')
        self.actor.load_state_dict(checkpoint['state_dict'])
        checkpoint = torch.load(f'{directory}/actor_target.pth.tar')
        self.actor_target.load_state_dict(checkpoint['state_dict'])
        checkpoint = torch.load(f'{directory}/critic.pth.tar')
        self.critic.load_state_dict(checkpoint['state_dict'])
        checkpoint = torch.load(f'{directory}/critic_target.pth.tar')
        self.critic_target.load_state_dict(checkpoint['state_dict'])
