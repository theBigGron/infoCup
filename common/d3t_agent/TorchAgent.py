import io
import json
import os
import logging
import tarfile
from typing import List, Tuple

from common.d3t_agent.ReplayMemory import ReplayBuffer
from common.d3t_agent.TD3Strategy import TD3
from common.data_processing import state_actions
from common.data_processing.tar_buffer import merge_models_tar_to_buffered_tar
from common.data_processing.state_actions import Actions
from common.data_processing.state_extractor import StateGenerator, merge_city_disease

INPUT_SIZE = 16


class TorchAgent:

    def __init__(self):
        """
        The TorchAgentClass holds a AI strategy for handling diseases and cities with their responding actions.
        It also saves game states and chosen actions for training after a game finished.
        """

        self.agent = TD3(state_dim=INPUT_SIZE,
                         action_dim=state_actions.get_number_of_actions())
        self.replay_memory: ReplayBuffer = ReplayBuffer()
        try:
            logging.info("======== PyTorchModel =========")
            if os.path.exists("models"):
                self.load()
            logging.info(" Pretrained model loaded")
        except FileNotFoundError as ex:
            logging.info(" No pretrained models availlable")

    def act(self, state: StateGenerator) -> List[Actions]:
        """
        Get all possible actions for current game state.

        :param state: Current game state.
        :return: List of all possible actions. Ordered by their activation.
        """
        result_list = []  # list of tuple (json_response, activation)

        # Calculate best disease action
        diseases = state.disease_info_list_of_dicts
        round_ = state.round

        # Calculate best City action
        cities = state.city_info_list_of_dicts
        result_list += self.get_actions(cities, diseases, round_)

        return result_list

    def get_actions(self, cities: dict, diseases: dict, round_: int) -> List[Actions]:
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
                self.replay_memory.add(
                    agent_input,
                    action=agent_output,
                    object_name=disease["name"] + city['city_name'],
                    round_=round_)
                city_action_list = Actions(city["city_name"],
                                           disease["name"],
                                           agent_input,
                                           agent_output,
                                           round_
                                           ).action_list
                result_list += city_action_list

        result_list.sort(key=lambda k: k[1], reverse=True)
        return result_list

    def train(self) -> None:
        """
        Trains the agent on actions chosen during this game with regards to the reward by the game outcome.
        """
        self.agent.train(self.replay_memory, iterations=3)
        self.replay_memory.flush()

    def update_reward(self, reward: float) -> None:
        """
        Updates entries in the replay buffer on the reward.
        :param reward: Quality of chosen decision.
        """
        self.replay_memory.update_reward(reward)

    # Return True wenn fehlerhaft
    def check_response(self, response_: json, game_json: json) -> bool:
        """
        Checks if the given move is a possible move.

        :param response_: Possible action to choose from.
        :param game_json: Current game state
        :return: Weather or not this move is a possible move.
        """
        if int(self.get_points(response_)) > game_json['points']:
            return True
        if response_['type'] == 'putUnderQuarantine':
            if response_['rounds'] > 0:
                return self.find_event_in_city(game_json, response_['city'], 'quarantine')
            else:
                return True
        if response_['type'] == 'closeAirport':
            if response_['rounds'] > 0:
                return self.find_event_in_city(game_json, response_['city'], 'airportClosed')
            else:
                return True
        if response_['type'] == 'closeConnection':
            if response_['rounds'] > 0:
                return self.find_event_in_city(game_json, response_['city'], 'connectionClosed')
            else:
                return True
        if response_['type'] == 'developVaccine':
            return self.find_develop(game_json, response_['pathogen'], 'vaccine', )
        if response_['type'] == 'deployVaccine':
            # Return False if vaccine is available and the city has this pathogen
            return self.find_deployment(game_json, response_['pathogen'], response_['city'], 'vaccine')
        if response_['type'] == 'developMedication':
            return self.find_develop(game_json, response_['pathogen'], 'medication', )
        if response_['type'] == 'deployMedication':
            # Return False if medication is available and the city has this pathogen
            return self.find_deployment(game_json, response_['pathogen'], response_['city'], 'medication')
        if response_['type'] == 'exertInfluence':
            return self.find_event_in_city(game_json, response_['city'], 'influenceExerted')
        if response_['type'] == 'callElections':
            return self.find_event_in_city(game_json, response_['city'], 'electionsCalled')
        if response_['type'] == 'applyHygienicMeasures':
            return self.find_event_in_city(game_json, response_['city'], 'hygienicMeasuresApplied')
        if response_['type'] == 'launchCampaign':
            return self.find_event_in_city(game_json, response_['city'], 'campaignLaunched')

    # TODO: Remove?
    def find_global_pathogen(self, game_json: json, pathogen_name: str, event_type: str) -> bool:
        """
        Searches if a pathogen exists in game.

        :param game_json: Current game state.
        :param pathogen_name: Name of the pathogen that gets searched for.
        :param event_type: Name of the event type that gets searched for.
        :return: Weather or not the specified pathogen exists during current game state.
        """
        for event in game_json['events']:
            if event['type'] == event_type:
                if event['pathogen']['name'] == pathogen_name:
                    return True
        return False

    def find_event_in_city(self, game_json, city, event_type) -> bool:
        """
        Searches if an event exists in a certain city.

        :param game_json: Current game state.
        :param city: City that we expect to contain an event.
        :param event_type: Type of event that we are looking for.
        :return:  False if city does not contain the event. False if the city neither exists nor contains the event.
        """
        for _, city_obj in game_json['cities'].items():
            if city_obj['name'] == city:
                if 'events' in city_obj:
                    for event in city_obj['events']:
                        if event['type'] == event_type:
                            # Wenn das Event existiert
                            return True
                # Wenn das Event nicht existiert
                return False
        # Wenn Stadt nicht gefunden wird
        return True

    def get_points(self, response_: json) -> int:
        """
        Retrieves the costs for an actions.

        :param response_: Action.
        :return: Points to spend.
        """
        points = dict()
        points['endRound'] = 0
        if 'rounds' in response_.keys():
            points['putUnderQuarantine'] = 10 * response_['rounds'] + 20
            points['closeAirport'] = 5 * response_['rounds'] + 15
            points['closeConnection'] = 3 * response_['rounds'] + 3
        points['developVaccine'] = 40
        points['deployVaccine'] = 5
        points['developMedication'] = 20
        points['deployMedication'] = 10
        points['exertInfluence'] = 3
        points['callElections'] = 3
        points['applyHygienicMeasures'] = 3
        points['launchCampaign'] = 3

        return points[response_['type']]

    def find_develop(self, game_json: json, pathogen_name: str, aid_type: str):
        """
        Looks if a medication or vaccine has been developed already.
        :param game_json: Current game state.
        :param pathogen_name: Name of the pathogen we would like to develop aid for.
        :param aid_type: Type of aid we would like to develop (Vaccione or Medication).
        :return: True if medication is in development.
        """
        # TODO: elif part not necessary.
        for event in game_json["events"]:
            if event['type'] == aid_type + 'InDevelopment':
                if event['pathogen']['name'] == pathogen_name:
                    return True
            elif event['type'] == aid_type + 'Available':
                if event['pathogen']['name'] == pathogen_name:
                    return False
        # Not developed
        return False

    # TODO: Is this method functioning?
    def find_deployment(self, game_json: json, pathogen_name: str, city: str, aid_type: str):
        """
        Looks if medicine has already been deployed in given city.
        :param game_json: Current state of the game.
        :param pathogen_name: Name of the pathogen.
        :param city: Name of the city.
        :param aid_type: Type of aid.
        :return: True if aid has been deployed.
        """
        for event in game_json["events"]:
            if event['type'] == aid_type + 'Available':
                if event['pathogen']['name'] == pathogen_name:
                    for city_name, city_obj in game_json['cities'].items():
                        if city_obj['name'] == city:
                            if 'events' in city_obj:
                                for event in city_obj['events']:
                                    if event['type'] == 'outbreak':
                                        if event['pathogen']['name'] == pathogen_name:
                                            return False
        return True

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
