import numpy as np
import logging


class ReplayBuffer:
    """
    Replay buffer for training.
    If training from DB it is advised to load multiple games before training.
    """

    def __init__(self):
        self.storage = []
        self.objects = dict()

    def add(self, state_old, action, object_name, round_, state_new=None, reward=None):
        """

        :param state_old: numpy array of state (nn input)
        :param action: resulting action
        :param state_new: numpy array of state (nn input) from the following round
        :param reward: reward after end of game
        :param object_name: City name or disease name
        :param round_: Current round of game
        :return: None
        """
        if object_name not in self.objects:
            self.objects[object_name] = []
        self.objects[object_name].append([state_old, state_new, action, reward, round_])

    def sample(self, batch_size):
        """
        Returns random samples
        Collecting random samples from replay buffer to avoid learning information that depends on predecessors.
        """
        if not self.storage:
            logging.debug("Empty Replay Buffer")
            for key in self.objects.keys():
                list_ = self.objects[key]
                self.storage += list_
        else:
            logging.debug("Buffer Filled")

        if batch_size == "all":
            batch_size = len(self.storage)

        random_indexes = np.random.randint(0, len(self.storage), size=batch_size)
        batch_states_old, batch_states_new, batch_actions, batch_rewards, = [], [], [], [],

        for i in random_indexes:
            state_old, state_new, action, reward, done = self.storage[i]
            batch_states_old.append(state_old)
            batch_states_new.append(state_new)
            batch_actions.append(action)
            batch_rewards.append(reward)

        return np.array(batch_states_old), np.array(batch_states_new), np.array(batch_actions), \
               np.array(batch_rewards).reshape(-1, 1)

    def update_reward(self, reward):
        """
        update reward
        """
        for object_ in self.objects.keys():
            list_transitions = self.objects[object_]
            list_transitions.sort(key=lambda k: k[4])
            for i, _ in enumerate(list_transitions):
                list_transitions[i][3] = reward
                if not i == len(list_transitions) - 1:
                    list_transitions[i][1] = list_transitions[i + 1][0]
            list_transitions = list_transitions[:-1]
            self.objects[object_] = list_transitions

    def save_buffer(self):
        """
        Saves Buffer to DataBase
        """
        pass

    def flush(self):
        """
        Saves and clears Buffer
        """
        self.storage = []
        self.objects = dict()
        logging.info("Clearing Storage and Objects.")
