import io
import os
import logging
import tarfile

from common.d3t_agent.ReplayMemory import ReplayBuffer
from common.d3t_agent.TD3Strategy import TD3
from common.data_processing.state_actions import CityActions, DiseaseActions
from common.data_processing.state_extractor import dis_dict_to_np, StateGenerator, merge_city_disease


class TorchAgent:

    def __init__(self):

        self.disease_agent = TD3(state_dim=7, action_dim=2, max_action=1)
        self.disease_replay_memory: ReplayBuffer = ReplayBuffer()

        self.city_agent = TD3(state_dim=10, action_dim=9, max_action=1)
        self.city_replay_memory: ReplayBuffer = ReplayBuffer()
        try:
            logging.info("======== PyTorchModel =========")
            if os.path.exists("models"):
                self.load()
            logging.info(" Pretrained model loaded")
        except FileNotFoundError as ex:
            logging.info(" No pretrained models availlable")

    def act(self, state: StateGenerator):
        result_list = []  # list of tuple (json_response, activation)

        # Calculate best disease action
        diseases = state.disease_info_list_of_dicts
        round_ = state.round
        result_list += self.get_disease_actions(diseases, round_)

        # Calculate best City action
        cities = state.city_info_list_of_dicts
        result_list += self.get_city_actions(cities, diseases, round_)

        # Evaluates all actions
        result_list.sort(key=lambda k: k[1], reverse=True)
        return result_list

    def get_disease_actions(self, diseases, round_: int):
        """
        Calculates most urgent action for diseases
        """
        result_list = []
        for disease in diseases:
            disease_np = dis_dict_to_np(disease)
            action = self.disease_agent.select_action(disease_np)  # Hier findet die Berechnung im Netz statt
            self.disease_replay_memory.add(disease_np,
                                           action=action,
                                           object_name=disease["name"],
                                           round_=round_)
            disease_action_list = DiseaseActions(disease["name"], action).action_list
            result_list += disease_action_list
        result_list.sort(key=lambda k: k[1])
        return result_list

    def get_city_actions(self, cities, diseases, round_: int):
        """
        Calculates most urgent action for cities
        """
        result_list = []

        for city in cities:

            for disease in diseases:
                city_with_disease = merge_city_disease(city, disease)
                action = self.city_agent.select_action(city_with_disease)
                self.city_replay_memory.add(city_with_disease,
                                            action=action,
                                            object_name=disease["name"] + city['city_name'],
                                            round_=round_)
                city_action_list = CityActions(city, disease, action).action_list
                result_list += city_action_list

        result_list.sort(key=lambda k: k[1])
        return result_list

    def train(self):
        self.city_agent.train(self.city_replay_memory, iterations=3)
        self.disease_agent.train(self.disease_replay_memory, iterations=3)
        self.city_replay_memory.flush()
        self.disease_replay_memory.flush()

    def update_reward(self, reward):
        self.city_replay_memory.update_reward(reward)
        self.disease_replay_memory.update_reward(reward)

    # Return True wenn fehlerhaft
    def check_response(self, response_, game_json):
        if int(self.get_points(response_)) > game_json['points']:
            return True
        if response_['type'] == 'putUnderQuarantine':
            if response_['rounds'] > 0:
                return self.find_event_in_city(game_json, response_['city'], 'quarantine')
            else:
                return True
        if response_['type'] == 'closeAirport':
            if [response_['rounds']] > 0:
                return self.find_event_in_city(game_json, response_['city'], 'airportClosed')
            else:
                return True
        if response_['type'] == 'closeConnection':
            if [response_['rounds']] > 0:
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

    def find_global_event(self, game_json, pathogen_name, typ):
        for event in game_json['events']:
            if event['type'] == typ:
                if event['pathogen']['name'] == pathogen_name:
                    # Event gefunden
                    return True
                # Event hat diesen Typ, aber für eine andere Krankheit
                return False
        # Kein Event von dem Typ
        return False

    def find_event_in_city(self, game_json, city, typ):
        for city_name, city_obj in game_json['cities'].items():
            if city_obj['name'] == city:
                if 'events' in city_obj:
                    for event in city_obj['events']:
                        if event['type'] == typ:
                            # Wenn das Event existiert
                            return True
                # Wenn das Event nicht existiert
                return False
        # Wenn Stadt nicht gefunden wird
        return True

    def get_points(self, response_):
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

    def find_develop(self, game_json, pathogen_name, typ):
        for event in game_json["events"]:
            if event['type'] == typ + 'InDevelopment':
                if event['pathogen']['name'] == pathogen_name:
                    return True
            elif event['type'] == typ + 'Available':
                if event['pathogen']['name'] == pathogen_name:
                    return False
        # Not developed
        return False

    def find_deployment(self, game_json, pathogen_name, city, typ):
        for event in game_json["events"]:
            if event['type'] == typ + 'Available':
                if event['pathogen']['name'] == pathogen_name:
                    for city_name, city_obj in game_json['cities'].items():
                        if city_obj['name'] == city:
                            if 'events' in city_obj:
                                for event in city_obj['events']:
                                    if event['type'] == 'outbreak':
                                        if event['pathogen']['name'] == pathogen_name:
                                            return False
        return True

    def get_models(self) -> list:
        model_list: list = self.city_agent.get_models("city") + self.disease_agent.get_models("disease")
        return model_list

    def get_models_as_tar_bin(self) -> tarfile.TarFile:
        models = self.get_models()
        outer_tar_buffer = io.BytesIO()
        tar = tarfile.TarFile(mode="w", fileobj=outer_tar_buffer)

        for model in models:
            model_class = model[0]
            model_type = model[1]
            model_bin = io.BytesIO(model[2])
            info = tarfile.TarInfo(name=f"{model_class}_{model_type}.pth.tar")
            info.size = len(model_bin.read())
            model_bin.seek(0)
            tar.addfile(tarinfo=info, fileobj=model_bin)
        tar.close()
        outer_tar_buffer.seek(0)
        return outer_tar_buffer




    def save(self, iteration_counter: int):
        iteration_counter = str(iteration_counter)
        self.city_agent.save("city", iteration_counter)
        self.disease_agent.save("disease", iteration_counter)

    def load(self, path=None):
        self.city_agent.load("city", path)
        self.disease_agent.load("disease", path)

    def load_bin(self, bin_models):
        city_models = []
        disease_models = []
        for model_info in bin_models:
            if "city" in model_info.name:
                city_models.append((bin_models.extractfile(model_info), model_info.name))
            elif "disease" in model_info.name:
                disease_models.append((bin_models.extractfile(model_info), model_info.name))
        self.city_agent.load_bin(city_models)
        self.disease_agent.load_bin(disease_models)