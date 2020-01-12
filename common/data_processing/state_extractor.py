from common.data_processing.utils import eval_disease_prevalence, eval_anti_vaccinationism

MAX_ROUNDS = 200  # replace mit logarithmus
MAX_AMOUNT_OF_CONNECTIONS = 20
MAX_POINTS = 100
SYM_VALUE_NORM_NUMBER_DICT = {
    '--': 0, '-': 0.25, 'o': 0.5, '+': 0.75, '++': 1
}


class GameState:

    def __init__(self, game_json):
        """
        Parses game state into a more concise format for faster access to needed information.

        :param game_json: ic20 json representing the current game state.
        """
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
                'anti-vaccinationism': eval_anti_vaccinationism(city_obj),
                'disease__prevalence': eval_disease_prevalence(city_obj)
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
        :return: 1 if type is available, (1,0) indicates the progress of development if in development, 0 otherwise
        """
        is_available = False
        is_in_development = False
        # This indicates the development progress based on the sinceRound/untilRound attr. in the global events
        # It is only be set/useful if the disease with disease_name is in development.
        dev_progress = -1
        for event in self.events:
            # Check if event type is typed development or availbility
            if event['type'] == type + 'InDevelopment':
                if event['pathogen']['name'] == disease_name:
                    is_in_development = True
                    dev_progress = float(event['sinceRound']) / float(event['untilRound'])
                    break
            elif event['type'] == type + 'Available':
                if event['pathogen']['name'] == disease_name:
                    is_available = True
                    break

        if is_available:
            return 1
        elif is_in_development:
            return dev_progress
        else:
            return 0

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

    def event_exists_in_city(self, city, event_type) -> bool:
        """
        Searches if an event exists in a certain city.

        :param game_json: Current game state.
        :param city: City that we expect to contain an event.
        :param event_type: Type of event that we are looking for.
        :return:  False if city does not contain the event nor exists. True if the city contains the event.
        """
        city_obj = self.game_json["cities"][city]
        if 'events' in city_obj:
            for event in city_obj['events']:
                if event['type'] == event_type:
                    # Wenn das Event existiert
                    return True
        # Wenn das Event nicht existiert
        return False

    def aid_in_development(self, pathogen_name: str, aid_type: str):
        """
        Looks if a medication or vaccine has been developed already.

        :param pathogen_name: Name of the pathogen we would like to develop aid for.
        :param aid_type: Type of aid we would like to develop (Vaccione or Medication).
        :return: True if medication is in development.
        """
        for event in self.events:
            if aid_type in event['type'] and 'InDevelopment' in event['type']:
                if event['pathogen']['name'] == pathogen_name:
                    return True
        # Not in development
        return False

    def aid_developed(self, pathogen_name: str, aid_type: str):
        """
        Looks if a medication or vaccine has been developed already.

        :param pathogen_name: Name of the pathogen we would like to develop aid for.
        :param aid_type: Type of aid we would like to develop (Vaccione or Medication).
        :return: True if medication is in development.
        """
        for event in self.events:
            if aid_type in event['type'] and 'Available' in event['type']:
                if event['pathogen']['name'] == pathogen_name:
                    return True
        return False

    def disease_in_city(self, city_name: str, pathogen_name: str ):
        """
        Checks if people are contaminated with a specific disease in a city.

        :param city_name: Name of City.
        :param pathogen_name: Name of Pathogen.
        :return: True if people are infected.
        """
        city_obj = self.game_json["cities"][city_name]
        if 'events' in city_obj:
            for event in city_obj['events']:
                if event['type'] == "outbreak":
                    if pathogen_name in event["pathogen"]["name"]:
                        return True
        return False

    def lock_down_over(self, city_name: str, event_type: str, round_: int):
        """
        Checks if a specific containment action is in progress in a given city.

        :param city_name: Name of city.
        :param event_type: Type of caontainment
        :param round_: Current round.
        :return: True if currently there is no containment of given city.
        """
        city_obj = self.game_json["cities"][city_name]
        if 'events' in city_obj:
            for event in city_obj['events']:
                if event_type in event['type']:
                    return round_ > event['untilRound']
        return True


