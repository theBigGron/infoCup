import numpy as np
from enum import Enum


class EnumCityActions(Enum):
    """
    Enum of City actions.
    Is sorted in the order of declaration.
    """
    endRound = '{"type":"endRound"}'
    putUnderQuarantine = '{{"type": "putUnderQuarantine", "city": "{city}", "rounds": {rounds}}}'
    excertInfluence = '{{"type": "exertInfluence", "city": "{city}"}}'
    callElections = '{{"type": "callElections", "city": "{city}"}}'
    applyHygienicMeasures = '{{"type": "applyHygienicMeasures", "city": "{city}" }}'
    launchCampaign = '{{"type": "launchCampaign", "city": "{city}" }}'
    deployMedication = '{{"type": "deployMedication", "pathogen": "{pathogen}", "city": "{city}" }}'
    deployVaccine = '{{"type": "deployVaccine", "pathogen": "{pathogen}", "city": "{city}" }}'


class CityActions:
    def __init__(self, city, pathogen, q: np.array):
        comb = zip(EnumCityActions, np.nditer(q[:-1]))
        self.action_list = []
        for x in comb:
            action = x[0].value
            if "pathogen" in action:
                action = action.format(city=city['city_name'], pathogen=pathogen['name'])
            elif "rounds" in action:
                rounds = (int(float(q[-1]) *30) if q[-1]>0 else 0)
                action = action.format(city=city['city_name'], rounds=rounds)
            elif "city" in action:
                action = action.format(city=city['city_name'])
            self.action_list.append((action, float(x[1])))
        self.action_list.sort(key=lambda k: k[1])

    def get_max_action(self):
        return self.action_list[0]


class EnumDiseaseActions(Enum):
    developVaccine = '{{"type": "developVaccine", "pathogen": "{pathogen}" }}'
    developMedication = '{{"type": "developMedication", "pathogen": "{pathogen}" }}'
    keys = [developVaccine, developMedication]


class DiseaseActions:
    """
    Takes pathogen and numpu array with probabilities
    and creates a tuple (response_json, probabillity)
    Example:
        ({"type": "developVaccine", "pathogen": "morbus marcellus" }, 0.1)
        Meaning develop vaccine for morbus marcellus has importance 0.1

    """
    def __init__(self, pathogen, q: np.array):
        comb = zip(EnumDiseaseActions, np.nditer(q))
        self.action_list = []
        for x in comb:
            action = x[0].value
            action = action.format(pathogen=pathogen)
            self.action_list.append((action, float(x[1])))

        self.action_list.sort(key=lambda k: k[1])

    def get_max_action(self):
        return self.action_list[0]

