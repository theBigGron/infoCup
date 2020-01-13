import json
from typing import Tuple, Any, Callable, List, Dict

import numpy as np
from numpy import ndarray
import logging

from common.data_processing.state_actions import ActionInfo


class ReplayBuffer:
    """
    Replay buffer for training.
    """

    def __init__(self):
        self.storage: List[ActionInfo] = []
        self.storage_buffer: List[ActionInfo] = []

    def add(self, action_info: ActionInfo = None, ):
        """
        Adds a transition to the replay buffer.

        :param action_info: ActionInfo containing the information about the move made.
        :return: None
        """
        assert isinstance(action_info, ActionInfo)
        self.storage_buffer.append(action_info)

    def add_bad_action(self, action_info: ActionInfo, punishment: float) -> None:
        """
        Does not add action to buffer but passes action directly to the storage.
        Punishment via highly negative reward.

        :param action_info: Action we were not able to do.
        :param punishment: Negative reward.
        :return: None
        """
        action_info.state_new = action_info.state
        action_info.reward = punishment
        self.storage.append(
            action_info
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
            info: ActionInfo = self.storage[i]
            batch_states_old.append(info.state)
            batch_states_new.append(info.state_new)
            batch_actions.append(info.action_out)
            batch_rewards.append(info.reward)

        return np.array(batch_states_old, dtype='float32'), \
               np.array(batch_states_new, dtype='float32'), \
               np.array(batch_actions, dtype='float32'), \
               np.array(batch_rewards, dtype='float32').reshape(-1, 1)

    def update_reward_and_clear(self, reward: float) -> None:
        """
        Update reward.
        Sorts all entries in the replay memory by round.
        Updates the reward for each entry in the memory. Divides reward by numbers of actions taken that turn.

        :param reward: Reward for selecting the actions currently buffered.
        :return: None
        """
        func: Callable[[ActionInfo], int] = lambda action_info: action_info.round_
        self.storage_buffer.sort(key=func)
        buffer: List[ActionInfo] = []
        round_ = self.storage_buffer[0].round_

        for action_info in self.storage_buffer:
            if action_info.round_ > round_:
                for buffered_info in buffer:
                    buffered_info.reward = reward/len(buffer)
                round_ = action_info.round_

            buffer.append(action_info)
        self.flush_buffer()

    def flush_buffer(self):
        """
        Saves and clears Buffer.
        """
        values = [row for row in self.storage_buffer if row.state_new is not None]
        self.storage.extend(values)
        self.storage_buffer: List[ActionInfo] = []
        logging.info("Clearing Storage and Objects.")

    def _retrieve_last_round_actions(self, relevant_round: int) -> List[ActionInfo]:
        """
        Returns all actions from last round to update their states.

        :param relevant_round:  Round from wich we need the states.
        :return: List of ActionInfos from requested round.
        """

        return [action_info for action_info in self.storage_buffer if action_info.round_ == relevant_round]

    def update_old_info_actions(self, new_actions: List[ActionInfo]) -> None:
        """
        Updates last rounds new_states with current rounds state.
        :param new_actions: ActionsInfo objects for new round.
        """

        actions_old = self._retrieve_last_round_actions(new_actions[0].round_ - 1)
        if not actions_old or actions_old[0].state_new is not None:
            #  Multiple moves in the same turn.
            return
        for old_action in actions_old:
            pathogen_info = None
            city_info = None
            for new_action in new_actions:
                # City still exists, so does the pathogene
                if old_action.city_name == new_action.city_name and \
                        old_action.pathogen_name == new_action.pathogen_name:
                    old_action.state_new = new_action.state
                    break
                if city_info is None and new_action.city_name == old_action.city_name:
                    city_info = new_action.state[0:8]
                    city_info = np.concatenate((city_info, np.zeros(1)))  # Disease prevalence must be 0 if disease does not exist.
                if pathogen_info is None and new_action.pathogen_name == old_action.pathogen_name:
                    pathogen_info = new_action.state[9:]

            if old_action.state_new is not None:
                continue
            if pathogen_info is None:
                pathogen_info = np.zeros(7)
            if city_info is None:
                city_info = np.zeros(9)
            old_action.state_new = np.concatenate((city_info, pathogen_info))
