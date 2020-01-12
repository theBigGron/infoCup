import json

import numpy as np

from common.data_processing.state_actions import ActionInfo


def dis_dict_to_np(elem):
    """
    Parses our disease dict into a numpy array representation
    .
    :param elem: Disease dict
    :return: Array representing the disease info state.
    """
    elem_value_list = [
        elem['vaccine_available_or_in_development'],
        elem['medication_available_or_in_development'],
        elem['duration'],
        elem['lethality'],
        elem['infectivity'],
        elem['mobility'],
        elem['world_prevalence']
    ]
    return np.array(elem_value_list)


def eval_disease_prevalence(city_obj):
    disease_prevalence = dict()
    if "events" in city_obj.keys():
        for event in city_obj["events"]:
            if event["type"] == "outbreak":
                disease_prevalence[event["pathogen"]["name"]] = event["prevalence"]
    return disease_prevalence


def city_dict_to_np_arr(city: dict, disease: str) -> np.ndarray:
    """
    Parses our city dict into a numpy array representation
    .
    :param elem: City dict
    :return: Array representing the city info state.
    """
    disease_prevalence = 0
    if 'disease_prevalence' in city.keys():
        if disease in city['disease_prevalence'].keys():
            disease_prevalence = city['disease__prevalence'][disease]
    elem_value_list = [
        city['population'],
        city['amount_connections'],
        city['connected_city_population'],
        city['economy'],
        city['government'],
        city['hygiene'],
        city['awareness'],
        city['anti-vaccinationism'],
        disease_prevalence,
    ]
    return np.array(elem_value_list)


def merge_city_disease(city: dict, disease: dict) -> np.ndarray:
    """
    Takes the actions for a city and combines them with the disease actions for that city.

    :param city: Dict of city actions and their activations.
    :param disease: Dict of disease actions and their activations.
    :return: Concatenated numpy array of actions.
    """
    city_out = city_dict_to_np_arr(city, disease["name"])
    disease_out = city_disease_info_to_np(disease)
    return np.concatenate((city_out, disease_out,), axis=None)


def city_disease_info_to_np(disease: dict):
    """
    Parses a disease information of a city from dict into a numpy array.

    :param disease: disease information of a city
    :return: Numpy array with world prevalence of disease and the diseases threat.
    """
    elem_value_list = [
        disease['duration'],
        disease['lethality'],
        disease['infectivity'],
        disease['mobility'],
        disease['world_prevalence'],
        disease['vaccine_available_or_in_development'],
        disease['medication_available_or_in_development']
    ]
    return np.array(elem_value_list)


def disease_threat(disease: dict):
    """
    Calculates the threat of a disease to the world population.

    :param disease: Disease dict.
    :return: Threat generated to the world.
    """

    return disease['world_prevalence'] * \
           (
                   (disease['duration']
                    + disease['lethality']
                    + disease['infectivity']
                    + disease['mobility'])
                   / 4
           )


def find_global_pathogen(game_json: json, pathogen_name: str, event_type: str) -> bool:
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


def _find_deployment(game_json: json, pathogen_name: str, city: str, aid_type: str):
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


def valid_response(action: ActionInfo, game_state: 'GameState'):
    """
    #Checks if the given move is a possible move.

    :param action: Possible action to choose from.
    :param game_state: Current game state
    :return: Weather or not this move is a possible move.
    """
    if "endRound" in action.server_message:
        return True
    if action.costs > game_state.points:
        return False
    if 'putUnderQuarantine' in action.server_message:
        return not game_state.event_exists_in_city(action.city_name, 'quarantine') and \
               not game_state.lock_down_over(action.city_name, 'quarantine', game_state.round)
    elif 'closeAirport' in action.server_message:
        return not game_state.event_exists_in_city(action.city_name, 'airportClosed') and \
               not game_state.lock_down_over(action.city_name, 'airportClosed', game_state.round)
    elif 'developVaccine' in action.server_message:
        return not game_state.aid_in_development(action.pathogen_name, 'vaccine', ) and \
               not game_state.aid_developed(action.pathogen_name, 'vaccine', )
    elif 'developMedication' in action.server_message:
        return not game_state.aid_in_development(action.pathogen_name, 'medication', ) and \
               not game_state.aid_developed(action.pathogen_name, 'medication', )

    elif 'deployVaccine' in action.server_message:
        return game_state.aid_developed(action.pathogen_name, 'vaccine', )
    elif 'deployMedication' in action.server_message:
        return game_state.aid_developed(action.pathogen_name, 'medication', ) and \
               game_state.disease_in_city(action.city_name, action.pathogen_name)
    return True


def eval_anti_vaccinationism(city_obj) -> int:
    """
    This method return 1 if a antiVaccinationism event was found in the cities event list, and 0 if not

    :param events: The events list from a city
    :return: 1 if a antiVaccinationism event was found in the cities event list, 0 if not
    """
    # Check if events list is already present in city_obj
    if 'events' not in city_obj:
        # If events list is not already present in city_obj, no 'antiVaccinationism' event was found,
        # so return 0
        return 0
    else:
        for event in city_obj['events']:
            if event['type'] == 'antiVaccinationism':
                # A 'antiVaccinationism'-event was found, so return 1 immediate
                return 1
        # No 'antiVaccinationism'-event was found, so return 0
        return 0
