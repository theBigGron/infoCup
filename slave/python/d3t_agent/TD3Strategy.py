import io
import os

import torch
import torch.nn.functional as F

from d3t_agent.Actor import Actor

from d3t_agent.Critic import Critic
from d3t_agent.ReplayMemory import ReplayBuffer

# Selecting the device (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL_PATH = "./pytorch_models"

if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)


class TD3:

    def __init__(self, state_dim, action_dim, max_action):
        # Loading actor and critic target
        self.actor = Actor(state_dim, action_dim, max_action).to(device)
        self.actor_target = Actor(state_dim, action_dim, max_action).to(device)
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters())
        # Loading critic and critic target
        self.critic = Critic(state_dim, action_dim).to(device)
        self.critic_target = Critic(state_dim, action_dim).to(device)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters())
        self.max_action = max_action
        self.action_dim = action_dim

    def select_action(self, state):
        state = torch.Tensor(state.reshape(1, -1)).to(device)
        res = self.actor(state).cpu().data.numpy().flatten()
        return res

    def train(self, replay_buffer: ReplayBuffer, iterations, batch_size=10000, discount=0.99, tau=0.005, policy_freq=2):

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
            next_action = (next_action).clamp(-self.max_action, self.max_action)

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
    def save(self, agent_type, dir_):
        """
        Save actual model from neuronal Network in with iretation counter
        also overrides current newest model.
        """
        for directory in ["max", dir_]:
            if not os.path.exists(f'{MODEL_PATH}/{directory}'):
                os.makedirs(f'{MODEL_PATH}/{directory}')
            actor_path = f'{MODEL_PATH}/{directory}/{agent_type}_actor.pth.tar'
            torch.save({'state_dict': self.actor.state_dict()}, actor_path)

            actor_target_path = f'{MODEL_PATH}/{directory}/{agent_type}_actor_target.pth.tar'
            torch.save({'state_dict': self.actor_target.state_dict()}, actor_target_path)

            critic_path = f'{MODEL_PATH}/{directory}/{agent_type}_critic.pth.tar'
            torch.save({'state_dict': self.critic.state_dict()}, critic_path)

            critic_target_path = f'{MODEL_PATH}/{directory}/{agent_type}_critic_target.pth.tar'
            torch.save({'state_dict': self.critic_target.state_dict()}, critic_target_path)

    def get_models(self, agent_type):
        model_list = []
        types_ = ["actor", "actor_target", "critic", "critic_target"]
        for ctr, model in enumerate([self.actor, self.actor_target, self.critic, self.critic_target]):
            buffer = io.BytesIO()
            torch.save({'state_dict': model.state_dict()}, buffer)
            data = buffer.getvalue()
            model_list.append((agent_type, types_[ctr], data))
        return model_list

    # Making a load method to load a pre-trained model
    def load(self, agent_type, directory=None):
        """
        load stored model from neuronal Network
        """
        if directory is not None:
            self.load_from_dir(agent_type, directory)
        else:
            if os.path.exists(f'{MODEL_PATH}/max'):
                self.load_from_dir(agent_type, "max")
            else:
                print("path does not exist")
                raise FileNotFoundError

    def load_bin(self, models: list):
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

    def load_from_dir(self, agent_type, directory):
        """
        load stored model for neural network from dir
        """
        checkpoint = torch.load(f'{MODEL_PATH}/{directory}/{agent_type}_actor.pth.tar')
        self.actor.load_state_dict(checkpoint['state_dict'])
        checkpoint = torch.load(f'{MODEL_PATH}/{directory}/{agent_type}_actor_target.pth.tar')
        self.actor_target.load_state_dict(checkpoint['state_dict'])
        checkpoint = torch.load(f'{MODEL_PATH}/{directory}/{agent_type}_critic.pth.tar')
        self.critic.load_state_dict(checkpoint['state_dict'])
        checkpoint = torch.load(f'{MODEL_PATH}/{directory}/{agent_type}_critic_target.pth.tar')
        self.critic_target.load_state_dict(checkpoint['state_dict'])
