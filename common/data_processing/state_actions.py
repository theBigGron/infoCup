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
    def __init__(self, city_name: str, pathogen: str, q: ndarray):
        comb = zip(EnumActions, nditer(q[1:]))

        self.action_list = []
        for x in comb:
            action = x[0].value
            if "pathogen" in action:
                if "city" in action:
                    action = action.format(city=city_name, pathogen=pathogen)
                else:
                    action = action.format(pathogen=pathogen)
            elif "rounds" in action:
                rounds = int((q[0] * 30))+1
                action = action.format(city=city_name, rounds=rounds)
            elif "city" in action:
                action = action.format(city=city_name)
            self.action_list.append((action, float(x[1])))
        self.action_list.sort(key=lambda k: k[1], reverse=True)

    def get_max_action(self):
        return self.action_list[0]
