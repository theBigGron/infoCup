import json
from typing import Tuple, Any

import numpy as np
from numpy import ndarray
import logging

from common.data_processing.state_actions import ActionInfo


class ReplayBuffer:
    """
    Replay buffer for training.
    """

    def __init__(self):
        self.storage = []
        self.storage_buffer = []

    def add(self, action_info: ActionInfo = None, ):
        """
        Adds a transition to the replay buffer.

        :param action_info: ActionInfo containing the information about the move made.
        :return: None
        """
        if action_info:
            self.storage_buffer.append({
                "state_old": action_info.state,
                "state_new": None,
                "action": action_info.action_out,
                "reward": None,
                "round": action_info.round_,
            })
        else:
            raise Exception

    def add_bad_action(self, action_info: ActionInfo, punishment: float) -> None:
        """
        Does not add action to buffer but passes action directly to the storage.
        Punishment via highly negative reward.

        :param action_info: Action we were not able to do.
        :param punishment: Negative reward.
        :return: None
        """
        self.storage.append(
            {
                "state_old": action_info.state,
                "state_new": action_info.state,
                "action": action_info.action_out,
                "reward": punishment,
                "round": action_info.round_,
            }
        )

    def sample(self, batch_size: int) -> Tuple[ndarray, ndarray, ndarray, Any]:
        """
        Returns random transition samples.

        Returns random transition samples from the memory buffer.
        Collecting random samples from replay buffer to avoid learning information that depends on predecessors.

        :param batch_size: Size of batch.
        :return: List of [old_state, new_state, action, reward]
        """

        if batch_size == "all" or batch_size >= len(self.storage):
            batch_size = len(self.storage)

        random_indexes = np.random.randint(0, len(self.storage), size=batch_size)
        batch_states_old, batch_states_new, batch_actions, batch_rewards, = [], [], [], [],

        for i in random_indexes:
            row = self.storage[i]
            state_old, state_new, action, reward = row["state_old"], row["state_new"], row["action"], row["reward"]
            batch_states_old.append(state_old)
            batch_states_new.append(state_new)
            batch_actions.append(action)
            batch_rewards.append(reward)

        return np.array(batch_states_old, dtype='float32'),\
               np.array(batch_states_new, dtype='float32'),\
               np.array(batch_actions, dtype='float32'), \
               np.array(batch_rewards, dtype='float32').reshape(-1, 1)

    def update_reward(self, reward: float) -> None:
        """
        Update reward.
        Sorts all entries in the replay memory by round.
        Updates the reward for each entry in the memory. Divides reward by numbers of actions taken that turn.

        :param reward: Reward for selecting the actions currently buffered.
        :return: None
        """
        self.storage_buffer.sort(key=lambda r: r["round"])
        buffer = []
        round_ = self.storage_buffer[0]["round"]

        for x in range(0, len(self.storage_buffer)-1,):
            self.storage_buffer[x]["reward"] = reward
            if self.storage_buffer[x]["round"] == round_:
                buffer.append(self.storage_buffer[x])
            else:
                for row in buffer:
                    row["state_new"] = self.storage_buffer[x]["state_old"]
                    row["reward"] = row["reward"]/len(buffer)
                round_ += 1
                buffer = [self.storage_buffer[x]]

        """        
        self.storage_buffer["state_new"]
        new_state = np.array(self.storage_buffer[x + 1]["state_old"], copy=True)
        self.storage_buffer[x]["state_new"] = new_state
        self.storage_buffer[x]["reward"] = reward
        """
        self.flush_buffer()

    def flush_buffer(self):
        """
        Saves and clears Buffer.
        """
        values = [row for row in self.storage_buffer if row["state_new"] is not None]
        self.storage.extend(values)
        self.storage_buffer = []
        logging.info("Clearing Storage and Objects.")
