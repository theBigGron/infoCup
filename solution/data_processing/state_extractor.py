import numpy as np
from memory_profiler import profile
MAX_ROUNDS = 200  # replace mit logarithmus
MAX_AMOUNT_OF_CONNECTIONS = 20
MAX_POINTS = 100
SYM_VALUE_NORM_NUMBER_DICT = {
    '--': 0, '-': 0.25, 'o': 0.5, '+': 0.75, '++': 1
}


class StateGenerator:

    def __init__(self, game_json):
        self.game_json = game_json
        self.round = game_json["round"]
        self.points = game_json["points"]
        self.cities = game_json["cities"]
        self.events = game_json["events"]
        self.city_info_list_of_dicts = []
        self.city_info_list_of_np_arr = []
        self.disease_info_list_of_dicts = []
        self.disease_info_list_of_np_arr = []
        self.world_population = 0
        self.calculate_world_population()
        self.build_city_info_list()
        #self.build_norm_global_info()
        self.build_norm_disease_info_list()
        self.response_list_cities = {"quarantine", "airportClosed", "connectionClosed", "vaccineInDeployment",
                                     "medicationInDeployment", "influenceExerted", "electionsCalled",
                                     "hygienicMeasuresApplied", "campaignLaunched"}
        self.response_list_global = {"vaccineInDevelopment", "medicationInDevelopment"}

    # /* *************** */
    # /*                 */
    # /*  Build methods  */
    # /*                 */
    # /* *************** */

    #def build_norm_global_info(self):
    #    # TODO Grab values from global events
    #    is_economic_crisis = False
    #    is_large_scale_panic = False
    #
    #    norm_global_info = [self.round / MAX_ROUNDS, self.points / MAX_POINTS, is_economic_crisis, is_large_scale_panic]
    #    return norm_global_info

    def build_norm_disease_info_list(self):
        # This is the list of all normed disease info
        # This will be: [[Vaccine_available_or_in_development=value,Medication_available_or_in_development=value, # 
        # duration=..., lethality=..., infectivity=..., mobility=..., world_prevalence], (0,0.125,0.25,0.5,0.75,1)
        # [...], ...] (without the qualifier in front of the values)
        # The ++, +, o, -, -- will be converted to a number
        self.disease_info_list_of_dicts = []
        # TODO Extract the disease-info from events as [Vaccine_available=value,Medication_available=value,
        #  duration=..., lethality=..., infectivity=...,mobility=...],
        #  add world_prevalence=sum(foreach(prevelance*population))/world_population and append them to norm_disease_info_list
        for id, event in enumerate(self.events):
            # This filters only the encountered disease events
            # In
            if event['type'] == 'pathogenEncountered':
                pathogen = event['pathogen']
                pathogen_name = pathogen['name']
                disease_info_dict = {
                    'id': id,
                    'name': pathogen_name,
                    'vaccine_available_or_in_development':
                        self.is_available_or_in_development_for_disease('vaccine', pathogen_name),
                    'medication_available_or_in_development':
                        self.is_available_or_in_development_for_disease('medication', pathogen_name),
                    'duration': SYM_VALUE_NORM_NUMBER_DICT[pathogen['duration']],
                    'lethality': SYM_VALUE_NORM_NUMBER_DICT[pathogen['lethality']],
                    'infectivity': SYM_VALUE_NORM_NUMBER_DICT[pathogen['infectivity']],
                    'mobility': SYM_VALUE_NORM_NUMBER_DICT[pathogen['mobility']],
                    'world_prevalence':
                    # This calcs the sum of the city prevalenced population for disease with patogen_name
                    # and norms it by world population
                        self.calc_sum_of_city_prevalenced_population_for_disease(pathogen_name) / self.world_population
                }
                # Append the dicts of individual diseases to the 'global' disease list
                self.disease_info_list_of_dicts.append(disease_info_dict)

    def build_city_info_list(self):
        # This is the list of all normed city info
        # This will be: [city_name = city_name, population=value/world_population,
        # amount_connections=value/20[norm zwischen 0-1] , connected_city_population=value/world_population,
        # economy=..., government=..., hygiene=..., awareness=...,[0-1 normieren]
        # anti-vaccinationism=..., disease_1_prevalence=..., ..., disease_n_prevalence=...], !n=10 wenn nicht 10, dann auffüllen mit 0 immer an die gleiche Stelle
        # [...], ...] (without the qualifier in front of the values)
        # The ++, +, o, -, -- will be converted to a number (0,0.125,0.25,0.5,0.75,1)
        self.city_info_list_of_dicts = []
        # TODO Extract the city-info from cities as
        #  economy=..., government=..., hygiene=..., awareness=..., calculate
        #  population=value/world_population,
        #  amount_connections=value/?, sum_connected_city_population=value/world_population, with world_population
        #  and extract anti-vaccinationism=..., disease_1_prevalence=..., ..., disease_n_prevalence=... of city-events
        for city_name, city_obj in self.cities.items():
            # Build dict of one city, use helper methods for additions values (e. g. world_population)
            city_info_dict = {
                'city_name': city_name,
                # Norm the population in regard to former calculated world_population
                'population': city_obj['population'] / self.world_population,
                # Count the connections and norm them by dividing through MAX_AMOUNT_OF_CONNECTIONS
                'amount_connections': len(city_obj['connections']) / MAX_AMOUNT_OF_CONNECTIONS,
                # This calculates the sum of the populations of the connected cities
                # and norms it by dividing with world_population
                'connected_city_population':
                    self.calculate_connected_cities_population(city_obj['connections']) / self.world_population,
                # These statements grab the value with given key from SYM_VALUE_NORM_NUMBER_DICT in order to
                # map --, ..., ++ to 0, ..., 1
                'economy': SYM_VALUE_NORM_NUMBER_DICT[city_obj['economy']],
                'government': SYM_VALUE_NORM_NUMBER_DICT[city_obj['government']],
                'hygiene': SYM_VALUE_NORM_NUMBER_DICT[city_obj['hygiene']],
                'awareness': SYM_VALUE_NORM_NUMBER_DICT[city_obj['awareness']],
                'anti-vaccinationism': self.eval_anti_vaccinationism(city_obj),
                # 'disease__prevalence':
            }
            # Append the dicts of individual cities to the 'global' city list
            self.city_info_list_of_dicts.append(city_info_dict)

    # /* ************************ */
    # /*                          */
    # /*  General helper methods  */
    # /*                          */
    # /* ************************ */

    def calculate_world_population(self):
        """
        This method calculates the world population by adding together all city populations
        """
        for city_name, city_obj in self.cities.items():
            self.world_population += city_obj["population"]

    # /* ********************* */
    # /*                       */
    # /*  City helper methods  */
    # /*                       */
    # /* ********************* */

    def calculate_connected_cities_population(self, connected_cities) -> int:
        """
        This method calculates the sum of the connected city populations
        
        :param connected_cities: The connected cities list in a city object
        :return: sum of the connected cities populations
        """
        connected_cities_population = 0
        for connected_city_name in connected_cities:
            connected_cities_population += self.cities[connected_city_name]['population']

        return connected_cities_population


    def eval_anti_vaccinationism(self, city_obj) -> int:
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

    #def convert_city_list_of_dicts_to_city_list_of_np_arr(self, list_of_dicts: list) -> list:
    #    list_of_np_arr = []
    #    for elem in list_of_dicts:
    #        # This gets the dict values as a list
    #        elem_value_list = self.city_dict_to_np_arr(elem)
    #        # This appends the np-arrayed dict value list to the list list_of_np_arr
    #        list_of_np_arr.append(elem_value_list)
    #    return list_of_np_arr

    # /* ************************ */
    # /*                          */
    # /*  Disease helper methods  */
    # /*                          */
    # /* ************************ */

    def calc_sum_of_city_prevalenced_population_for_disease(self, disease_name):
        sum_of_city_prevalenced_population = 0
        # Iterate over the events in cities
        for city_name, city_obj in self.cities.items():
            if 'events' in city_obj:
                for event in city_obj['events']:
                    # If the disired disease (id. by disease_name) is encountered in city (outbreak)
                    if event['type'] == 'outbreak' and event['pathogen']['name'] == disease_name:
                        # Calculate the amount of affected people in the city
                        sum_of_city_prevalenced_population += event['prevalence'] * city_obj['population']
        return sum_of_city_prevalenced_population


    def is_available_or_in_development_for_disease(self, type, disease_name) -> int:
        """
        This method returns the availbility ORed with the development of the types status

        :param type: The type of a anti-disease action, MAY ONLY be 'vaccine' or 'medication'
        :param disease_name: The name of a disease, MAY ONLY be one of all name of diseases
        :return: 1 if type is available or in development, 0 otherwise
        """
        is_available = False
        is_in_development = False
        for event in self.events:
            # Check if event type is typed development or availbility
            if event['type'] == type + 'InDevelopment':
                if event['pathogen']['name'] == disease_name:
                    is_in_development = True
                    break
            elif event['type'] == type + 'Available':
                if event['pathogen']['name'] == disease_name:
                    is_available = True
                    break

        if is_available or is_in_development:
            return 1
        else:
            return 0

    #def convert_disease_list_of_dicts_to_disease_list_of_np_arr(self, list_of_dicts: list) -> list:
    #    list_of_np_arr = []
    #    for elem in list_of_dicts:
    #        # This gets the dict values as a list
    #        elem_value_list = self.dis_dict_to_np(elem)
    #        # This appends the np-arrayed dict value list to the list list_of_np_arr
    #        list_of_np_arr.append(np.array(elem_value_list))
    #    return list_of_np_arr

    #def convert_disease_to_list(self, disease: dict):
    #    return np.array(list(disease.items(), dtype=[('id', 'u')]))

    # /* ************************ */
    # /*                          */
    # /*  Game helper methods     */
    # /*                          */
    # /* ************************ */

    def move_done(self) -> bool:
        """
        Method should check if a move was done
        :param self:
        :return:
        """
        # check for every city in city
        for city_name, city_obj in self.cities.items():
            if 'events' in city_obj:
                for event in city_obj['events']:
                    if event['type'] in self.response_list_cities:
                        if 'sinceRound' in event:
                            if event['sinceRound'] == self.round:
                                return True
                        if 'round' in event:
                            if event['round'] == self.round:
                                return True

        # check for global events
        for event in self.events:
            if event["type"] in self.response_list_global:
                if event["sinceRound"] == self.round:
                    return True
        return False

    def get_errors(self):
        return self.game_json["error"]


def city_dict_to_np_arr(elem):
    elem_value_list = [
        elem['population'],
        elem['amount_connections'],
        elem['connected_city_population'],
        elem['economy'],
        elem['government'],
        elem['hygiene'],
        elem['awareness'],
        elem['anti-vaccinationism']
    ]
    return np.array(elem_value_list)


def dis_dict_to_np(elem):
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


def merge_city_disease(city, disease):
    city = city_dict_to_np_arr(city)
    disease = city_disease_info(disease)
    return np.concatenate((city, disease,), axis=None)


def city_disease_info(disease):
    elem_value_list = [
        disease['world_prevalence'],
        disease_threat(disease)
    ]
    return np.array(elem_value_list)


def disease_threat(disease):
    sum = disease['world_prevalence'] * \
          (
                  (disease['duration']
                   + disease['lethality']
                   + disease['infectivity']
                   + disease['mobility'])
                  / 4
          )
    return sum
