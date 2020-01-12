import io
import tarfile
from random import random, choice
from typing import List, Tuple

from common.d3t_agent.ReplayMemory import ReplayBuffer
from common.d3t_agent.TD3Strategy import TD3
from common.data_processing import state_actions
from common.data_processing.tar_buffer import merge_models_tar_to_buffered_tar
from common.data_processing.state_actions import Actions, ActionInfo
from common.data_processing.state_extractor import GameState
from common.data_processing.utils import merge_city_disease, valid_response

INPUT_SIZE = 16


class TorchAgent:

    def __init__(self):
        """
        The TorchAgentClass holds a AI strategy for handling diseases and cities with their responding actions.
        It also saves game states and chosen actions for training after a game finished.
        """

        self.agent = TD3(state_dim=INPUT_SIZE,
                         action_dim=len(state_actions.ENUM_ACTIONS) + 1)
        self.replay_memory: ReplayBuffer = ReplayBuffer()
        self.exploration_rate: float = 1

    def act(self, state: GameState) -> str:
        """
        Get all possible actions for current game state.

        :param state: Current game state.
        :return: List of all possible actions. Ordered by their activation.
        """
        try:
            cities = state.city_info_list_of_dicts
            diseases = state.disease_info_list_of_dicts
            round_ = state.round


            result_list = self._get_actions(cities, diseases, round_)

            action = self.select_action(result_list, state)

            response = action.server_message
            print(response)
            if "endRound" in response:
                print(" ")

        except Exception as ex:
            a = ex
            print("hi")
        return response

    def select_action(self, action_list: List[ActionInfo], state: GameState) -> ActionInfo:
        """
        Takes action from list. Either greedy or with a certain chance a random action.
        If the action is useful it returns it to ic20 and saves it to the replay memory buffer. Otherwise it is added to
        the bad decision list.

        :param action_list: List of all possible action before validation.
        :param state: Current state of the game.
        :return: Selected action. Has been validated.
        """
        choice_counter = 0
        explore = random() < self.exploration_rate
        while True:
            if not explore:
                action = action_list[choice_counter]
                choice_counter += 1
            else:
                action = choice(action_list)

            if valid_response(action, state):
                self._action_selected(action)
                return action
            else:
                self._bad_action(action)

    def _get_actions(self, cities: dict, diseases: dict, round_: int) -> List[Actions]:
        """
        Calculates most urgent action for cities.
        Saves current state and actions for each possible action to replay buffer.

        :return result_list: List of all possible actions with their corresponding activation. Sorted by activation.
        """
        result_list = []

        for city in cities:

            for disease in diseases:
                agent_input = merge_city_disease(city, disease)
                agent_output = self.agent.select_action(agent_input)

                city_action_list = Actions(city["city_name"],
                                           disease["name"],
                                           agent_input,
                                           agent_output,
                                           round_
                                           ).action_list
                result_list += city_action_list

        result_list.sort(reverse=True)
        return result_list

    def _action_selected(self, action_info: ActionInfo):
        """
        Saves action for later training. Action still needs its reward to be calculated.
        :param action_info: Select action for later training.
        """
        self.replay_memory.add(action_info)

    def _bad_action(self, action: ActionInfo):
        """
        Bad action the agent should get punished for.
        :param action: Bad action.
        """
        self.replay_memory.add_bad_action(action, -1.)

    def train(self) -> None:
        """
        Trains the agent on actions chosen during this game with regards to the reward by the game outcome.
        """
        self.agent.train(self.replay_memory, iterations=10)
        self.replay_memory.flush_buffer()

    def update_reward(self, reward: float) -> None:
        """
        Updates entries in the replay buffer on the reward.
        :param reward: Quality of chosen decision.
        """
        self.replay_memory.update_reward(reward)

    def get_models(self) -> List[Tuple[str, str, bytes]]:
        """
        Retrieves models for both types of agents.

        :return: List of all models trained by this agent.
        """
        model_list: list = self.agent.get_models()
        return model_list

    def get_models_as_tar_bin(self) -> io.BytesIO:
        """
        Collects all models and merges them in an outer tar file.
        Returns that tar File as binary buffer.
        :return: TarFile as BytesIO.
        """
        outer_tar_buffer = merge_models_tar_to_buffered_tar(self.get_models())
        return outer_tar_buffer

    def save(self, iteration_counter: int):
        """
        Saves current models to pth file.

        :param iteration_counter: Iterations the model trained for.
        :return: Model weights saved in pth file.
        """
        iteration_counter = str(iteration_counter)
        self.agent.save(iteration_counter)

    def load(self, path: str = None) -> None:
        """
        Load weights for models from path.
        :param path: Path where the models are saved.
        :return: None
        """
        self.agent.load(path)

    def load_bin(self, bin_models: tarfile.TarFile) -> None:
        """
        Loads model weights form a tar file (binary form) into our models.

        :param bin_models: Tar File containing model weights as io.BytesIO
        :return: None
        """
        city_models = []
        for model_info in bin_models:
            city_models.append((bin_models.extractfile(model_info), model_info.name))
        self.agent.load_bin(city_models)
