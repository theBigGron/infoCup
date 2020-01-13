from collections import OrderedDict

from numpy import ndarray, nditer

ENUM_ACTIONS = [
    {"message": '{type:"endRound"}', "fixed_costs": 0, "variable_costs": 0},
    {"message": '{{"type": "putUnderQuarantine", "city": "{city}", "rounds": {rounds}}}',
     "fixed_costs": 10, "variable_costs": 20},
    {"message": '{{"type": "closeAirport", "city": "{city}", "rounds": {rounds}}}',
     "fixed_costs": 5, "variable_costs": 15},
    {"message": '{{"type": "exertInfluence", "city": "{city}"}}', "fixed_costs": 3, "variable_costs": 0},
    {"message": '{{"type": "callElections", "city": "{city}"}}', "fixed_costs": 3, "variable_costs": 0},
    {"message": '{{"type": "applyHygienicMeasures", "city": "{city}" }}', "fixed_costs": 3, "variable_costs": 0},
    {"message": '{{"type": "launchCampaign", "city": "{city}" }}', "fixed_costs": 3, "variable_costs": 0},
    {"message": '{{"type": "deployMedication", "pathogen": "{pathogen}", "city": "{city}" }}',
     "fixed_costs": 10, "variable_costs": 0},
    {"message": '{{"type": "deployVaccine", "pathogen": "{pathogen}", "city": "{city}" }}',
     "fixed_costs": 5, "variable_costs": 0},
    {"message": '{{"type": "developVaccine", "pathogen": "{pathogen}" }}', "fixed_costs": 40, "variable_costs": 0},
    {"message": '{{"type": "developMedication", "pathogen": "{pathogen}" }}', "fixed_costs": 20, "variable_costs": 0},
]


class Actions:
    """
    Creates a collection of all moves possible in regards to the passed city.
    Creates a json that can be send to the simulation.
    q len must be len(EnumActions)+1

    """

    def __init__(self, city_name: str, pathogen: str, state: ndarray, action_out: ndarray, round_):
        self.action_list = []

        for activation_index, activation in enumerate(action_out[1:]):
            rounds_ = abs(int((action_out[0] * 30))) + 1
            action_info = ActionInfo(city_name=city_name,
                                     pathogen_name=pathogen,
                                     state=state,
                                     action_out=action_out,
                                     activation=activation,
                                     action=ENUM_ACTIONS[activation_index],
                                     round_=round_,
                                     rounds_=rounds_,
                                     )
            self.action_list.append(action_info)
        self.action_list.sort(reverse=True)


class ActionInfo:

    def __init__(self,
                 city_name: str,
                 pathogen_name: str,
                 state: ndarray,
                 action_out: ndarray,
                 activation: float,
                 action: dict,
                 rounds_: int,
                 round_: int):

        self.city_name = city_name
        self.pathogen_name = pathogen_name
        self.round_ = round_
        self.state = state
        self.action_out = action_out
        self.rounds_ = rounds_
        self.activation = float(activation)
        self.costs = action["fixed_costs"] + action["variable_costs"] * self.rounds_
        self.server_message = self.format_message(action["message"])

        # To be added Later
        self.state_new = None  # added in round self.round_+1
        self.reward = None  # added after game

    def __lt__(self, other):
        return self.activation < other.activation

    def __eq__(self, other):
        return self.activation == other.activation

    def __ge__(self, other):
        return not self.__lt__(other) or self.__eq__(other)

    def format_message(self, message):
        action = message
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
