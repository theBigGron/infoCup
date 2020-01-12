import unittest
from unittest import TestCase


class Test(TestCase):
    def test_valid_response(self):
        self.fail()

    @unittest.skip("Old API")
    def test_end_round(self):
        response = {'type': 'endRound'}
        self.assertFalse(check_response(response, game_json))

    """
    This method tries to perform an action "putUnderQuarantine". The number of rounds (45) is so high that the required
    points (470) are greater than the points available (309).

    10 * 45 + 20 = 470 points

    So the method check_response has to return a True, because there is a logical mistake in the response.
    """

    @unittest.skip("Old API")
    def test_not_enough_points(self):
        response = {'type': 'putUnderQuarantine', 'city': 'Accra', 'rounds': 45}
        self.assertTrue(check_response(response, game_json))

    """
    This method tries to perform an action "callElections". The existing points (309) are sufficient to carry out the 
    action. The action requires only (3) points.

    10 * 45 + 20 = 470 points

    So the method check_response has to return a False, because there is no logical mistake in the response.
    """

    @unittest.skip("Old API")
    def test_enough_points(self):
        response = {'type': 'putUnderQuarantine', 'city': 'Accra', 'rounds': 1}
        self.assertFalse(check_response(response, game_json))

    """
    This test serves to check whether it is possible to execute an action for 0 laps. Because it is not logical to 
    quarantine a city for 0 laps.
    """

    @unittest.skip("Old API")
    def test_zero_rounds(self):
        response = {'type': 'putUnderQuarantine', 'city': 'Accra', 'rounds': 0}
        self.assertTrue(check_response(response, game_json))

    """
    This method tries to quarantine a city. To do this, the action "putUnderQurantine" should be executed. Since a city 
    cannot be quarantined twice, the system checks if the city already has an event that indicates that the city is 
    quarantined.
    """

    @unittest.skip("Old API")
    def test_put_under_putUnderQuarantine(self):
        response = {'type': 'putUnderQuarantine', 'city': 'New York City', 'rounds': 2}
        self.assertTrue(check_response(response, game_json))

    """
    This test tries to perform an action "closeAirport" which will close an airport.
    The method "check_response" must return false, because there is no logical error in this scenario.
    """

    @unittest.skip("Old API")
    def test_close_airport(self):
        response = {'type': 'closeAirport', 'city': 'Abuja', 'rounds': 2}
        self.assertFalse(check_response(response, game_json))

    """
    This test tries to perform an action "closeAirport" which will close an airport.
    The method "check_response" must return true, because there is a logical error in this scenario. The airport is 
    already closed.
    """

    @unittest.skip("Old API")
    def test_close_closed_airport(self):
        response = {'type': 'closeAirport', 'city': 'New York City', 'rounds': 2}
        self.assertTrue(check_response(response, game_json))

    """
    This test attempts to execute action "exertInfluence". Since this action has not yet been executed in the city where 
    the action is to be executed, the method "check_response" must return a false.
    """

    @unittest.skip("Old API")
    def test_wrong_exert_influence(self):
        response = {'type': 'exertInfluence', 'city': 'Anchorage', 'rounds': 2}
        self.assertTrue(check_response(response, game_json))

    """
    This test attempts to execute action "exertInfluence". Since this action has already been executed in the city where 
    the action is to be executed, the method "check_response" must return a true.
    """

    @unittest.skip("Old API")
    def test_exert_influence(self):
        response = {'type': 'exertInfluence', 'city': 'Abuja', 'rounds': 2}
        self.assertFalse(check_response(response, game_json))

    """
    This test attempts to execute action "callElections". Since this action has already been executed in the city where 
    the action is to be executed, the method "check_response" must return a true.
    """

    @unittest.skip("Old API")
    def test_wrong_call_elections(self):
        response = {'type': 'callElections', 'city': 'Abuja', 'rounds': 2}
        self.assertTrue(check_response(response, game_json))

    """
    This test attempts to execute action "callElections". Since this action has not yet been executed in the city where 
    the action is to be executed, the method "check_response" must return a false.
    """

    @unittest.skip("Old API")
    def test_call_elections(self):
        response = {'type': 'callElections', 'city': 'Accra', 'rounds': 2}
        self.assertFalse(check_response(response, game_json))

    """
    This test attempts to execute action "applyHygienicMeasures". Since this action has not yet been executed in the 
    city where the action is to be executed, the method "check_response" must return a false.
    """

    @unittest.skip("Old API")
    def test_apply_hygienic_measures(self):
        response = {'type': 'applyHygienicMeasures', 'city': 'Abuja', 'rounds': 2}
        self.assertFalse(check_response(response, game_json))

    """
    This test attempts to execute action "applyHygienicMeasures". Since this action has already been executed in the 
    city where the action is to be executed, the method "check_response" must return a true.
    """

    @unittest.skip("Old API")
    def test_wrong_apply_hygienic_measures(self):
        response = {'type': 'applyHygienicMeasures', 'city': 'Portland', 'rounds': 2}
        self.assertTrue(check_response(response, game_json))

    """
    This test attempts to execute action "launchCampaign". Since this action has already been executed in the 
    city where the action is to be executed, the method "check_response" must return a true.
    """

    @unittest.skip("Old API")
    def test_wrong_launch_campaign(self):
        response = {'type': 'launchCampaign', 'city': 'Abuja', 'rounds': 2}
        self.assertTrue(check_response(response, game_json))

    """
    This test attempts to execute action "launchCampaign". Since this action has not yet been executed in the city where 
    the action is to be executed, the method "check_response" must return a false.
    """

    @unittest.skip("Old API")
    def test_launch_campaign(self):
        response = {'type': 'launchCampaign', 'city': 'New York City', 'rounds': 2}
        self.assertFalse(check_response(response, game_json))

    """
    This test serves to check whether a disease exists globally. To do this, the type of event (pathogenEncountered) and
    the name of the disease are required. If the disease exists, the value true should be returned.
    """

    @unittest.skip("Old API")
    def test_existing_global_pathogen(self):
        pathogen_name = "Admiral Trips"
        type = "pathogenEncountered"
        self.assertTrue(find_global_pathogen(game_json, pathogen_name, type))

    """
    This test serves to check whether a disease not exists globally. To do this, the type of event (pathogenEncountered) 
    and the name of the disease are required. If the disease not exists, the value false should be returned.
    """

    @unittest.skip("Old API")
    def test_not_existing_global_pathogen(self):
        pathogen_name = "Neurodermantotitis"
        type = "pathogenEncountered"
        self.assertFalse(find_global_pathogen(game_json, pathogen_name, type))

    """
    The method "find_event_in_city", is used to check whether an action has already been executed in a city. The test 
    checks directly in three different cities whether the existing events are found there.
    """

    @unittest.skip("Old API")
    def test_existing_event_in_city(self):
        first_city = "Abuja"
        first_event = "campaignLaunched"

        second_city = "Albuquerque"
        second_event = "outbreak"

        third_city = "Portland"
        third_event = "hygienicMeasuresApplied"

        self.assertTrue(_find_event_in_city(game_json, first_city, first_event))
        self.assertTrue(_find_event_in_city(game_json, second_city, second_event))
        self.assertTrue(_find_event_in_city(game_json, third_city, third_event))

    """
    The method "find_event_in_city", is used to check whether an action has already been executed in a city. The test 
    checks directly in three different cities whether the non-existent events are found. Since the events do not exist, 
    a false should be returned.
    """

    @unittest.skip("Old API")
    def test_not_existing_event_in_city(self):
        first_city = "Abuja"
        first_event = "worldPiece#"

        second_city = "Albuquerque"
        second_event = "moneyRain"

        third_city = "Portland"
        third_event = "taxReduction"

        self.assertFalse(_find_event_in_city(game_json, first_city, first_event))
        self.assertFalse(_find_event_in_city(game_json, second_city, second_event))
        self.assertFalse(_find_event_in_city(game_json, third_city, third_event))

    """
    There are two global events, one for vaccines and one for drugs. While these things are being developed, they are 
    not yet available. The test ensures that this is detected and therefore no distribution requests are sent out while 
    it is still inDevelopment.
    The test should return True if it is still in development.
    """

    @unittest.skip("Old API")
    def test_find_existing_in_develop(self):
        first_pathogen_name = "Phagum vidiianum"
        first_type = "vaccine"

        second_pathogen_name = "Admiral Trips"
        second_type = "medication"

        self.assertTrue(_find_develop(game_json, first_pathogen_name, first_type))
        self.assertTrue(_find_develop(game_json, second_pathogen_name, second_type))

    """
    This test checks whether the "find_develop" method finds development for pathogens that do not exist. Since there 
    is a logical error, the return value should be False.
    """

    @unittest.skip("Old API")
    def test_find_not_existing_in_develop(self):
        first_pathogen_name = "moneyRain"
        first_type = "vaccine"

        second_pathogen_name = "texReduction"
        second_type = "medication"

        self.assertFalse(_find_develop(game_json, first_pathogen_name, first_type))
        self.assertFalse(_find_develop(game_json, second_pathogen_name, second_type))

    """
    As soon as a drug or vaccine is available, it is globally advertised as "Available". The method checks whether this 
    is also found. Since this is logically correct, the method should return False.
    """

    @unittest.skip("Old API")
    def test_find_existing_available(self):
        first_pathogen_name = "Procrastinalgia"
        first_type = "vaccine"

        second_pathogen_name = "Methanobrevibacter colferi"
        second_type = "medication"

        self.assertFalse(_find_develop(game_json, first_pathogen_name, first_type))
        self.assertFalse(_find_develop(game_json, second_pathogen_name, second_type))

    """
    To be able to distribute a medicine or vaccine, it must be available globally and the desired city must also be 
    infected with the disease for which the vaccine / medicine was developed. Since the medicine and vaccine are 
    available, it can be distributed in the city. Return value should therefore be False.
    """

    @unittest.skip("Old API")
    def test_find_correct_deployment(self):
        pathogen_name = "Methanobrevibacter colferi"
        city = "Abuja"

        first_type = "vaccine"
        second_type = "medication"

        self.assertFalse(_find_deployment(game_json, pathogen_name, city, first_type))
        self.assertFalse(_find_deployment(game_json, pathogen_name, city, second_type))