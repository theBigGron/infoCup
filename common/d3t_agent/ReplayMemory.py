import json
from typing import Tuple, Any

import numpy as np
from numpy import ndarray
import logging


class ReplayBuffer:
    """
    Replay buffer for training.
    """

    def __init__(self):
        self.storage = []
        self.objects = dict()

    def add(self,
            state_old: ndarray,
            action: dict,
            object_name: str,
            round_: int,
            state_new: Any = None,
            reward: Any = None):
        """
        Adds a transition to the replay buffer.

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

    def sample(self, batch_size: int) -> Tuple[ndarray, ndarray, ndarray, Any]:
        """
        Returns random transition samples.

        Returns random transition samples from the memory buffer.
        Collecting random samples from replay buffer to avoid learning information that depends on predecessors.

        :param batch_size: Size of batches.
        :return: List of [old_state, new_state, action, reward]
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

    def update_reward(self, reward: float) -> None:
        """
        Update reward.
        Sorts all entries in the replay memory by round.
        Updates the reward for each entry in the memory.

        :param reward: Reward for selecting the actions currently buffered.
        :return: None  np.array,
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

    def flush(self):
        """
        Saves and clears Buffer.
        """
        self.storage = []
        self.objects = dict()
        logging.info("Clearing Storage and Objects.")
