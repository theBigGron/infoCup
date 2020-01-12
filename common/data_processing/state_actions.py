from numpy import ndarray, nditer
from enum import Enum


class EnumActions(Enum):
    """
    Enum of City actions.
    Is sorted in the order of declaration.
    """
    endRound = '{"type":"endRound"}'
    putUnderQuarantine = '{{"type": "putUnderQuarantine", "city": "{city}", "rounds": {rounds}}}'
    closeAirport = '{{"type": "closeAirport", "city": "{city}", "rounds": {rounds}}}'
    excertInfluence = '{{"type": "exertInfluence", "city": "{city}"}}'
    callElections = '{{"type": "callElections", "city": "{city}"}}'
    applyHygienicMeasures = '{{"type": "applyHygienicMeasures", "city": "{city}" }}'
    launchCampaign = '{{"type": "launchCampaign", "city": "{city}" }}'
    deployMedication = '{{"type": "deployMedication", "pathogen": "{pathogen}", "city": "{city}" }}'
    deployVaccine = '{{"type": "deployVaccine", "pathogen": "{pathogen}", "city": "{city}" }}'
    developVaccine = '{{"type": "developVaccine", "pathogen": "{pathogen}" }}'
    developMedication = '{{"type": "developMedication", "pathogen": "{pathogen}" }}'


def get_number_of_actions() -> int:
    """
    :return: Required size of numpy array to use EnumActions
    """
    return len(EnumActions)+1


class Actions:
    """
    Creates a collection of all moves possible in regards to the passed city.
    Creates a json that can be send to the simulation.
    q len must be len(EnumActions)+1

    """
    def __init__(self, city_name: str, pathogen: str, state: ndarray, action_out: ndarray, round):
        self.action_list = []
        for x, entry in EnumActions:
            a = ActionInfo(city_name, pathogen, server_message=EnumActions[x])

            action = x[0].value
            rounds = int((action_out[0] * 30)) + 1
            self.action_list.append((action, float(x[1])))
        self.action_list.sort(key=lambda k: k[1], reverse=True)

    def get_max_action(self):
        return self.action_list[0]


class ActionInfo:

    def __init__(self,
                 city_name: str,
                 pathogen_name: str,
                 state: ndarray,
                 action: ndarray,
                 rounds_: str,
                 activation: float,
                 server_message: str):

        self.city_name = city_name
        self.pathogen_name = pathogen_name
        self.state = state
        self.action = action
        self.rounds_ = rounds_
        self.activation = activation
        self.server_message = self.format_message(server_message)

    def format_message(self, message):
        action = ""
        if "pathogen" in message:
            if "city" in message:
                action = message.format(city=self.city_name, pathogen=self.pathogen_name)
            else:
                action = message.format(pathogen=self.pathogen_name)
        elif "rounds" in message:

            action = message.format(city=self.city_name, rounds=self.rounds_)
        elif "city" in message:
            action = message.format(city=self.city_name)
        return action

