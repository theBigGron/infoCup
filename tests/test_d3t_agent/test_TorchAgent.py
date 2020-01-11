import filecmp
import unittest
import os.path
import json
from distutils.dir_util import copy_tree
from common.d3t_agent.TorchAgent import TorchAgent
from common.data_processing.state_extractor import StateGenerator
from tests.data_for_tests import GameJson
from os import path

game_json = GameJson.game_json
agent = TorchAgent()

"""
Important!

Every testmethod must start with a lowercase "test_" enough
For example: test_not_enough_points

If you need a game json, there is a class "GameJson.py" where you can find a shorter version of the original jame json 
from the ic_20 tool.

This class contains the tests for the class Actor.
"""


class TorchAgentTest(unittest.TestCase):
    """
    This method tests the response for an "endRound". For this action we need no points.
    Because we need (0) points, the method check_response has to return a False, because there is no logical mistake in
    the response
    """

    def test_end_round(self):
        response = {'type': 'endRound'}
        self.assertFalse(agent.check_response(response, game_json))

    """
    This method tries to perform an action "putUnderQuarantine". The number of rounds (45) is so high that the required
    points (470) are greater than the points available (309).

    10 * 45 + 20 = 470 points

    So the method check_response has to return a True, because there is a logical mistake in the response.
    """

    def test_not_enough_points(self):
        response = {'type': 'putUnderQuarantine', 'city': 'Accra', 'rounds': 45}
        self.assertTrue(agent.check_response(response, game_json))

    """
    This method tries to perform an action "callElections". The existing points (309) are sufficient to carry out the 
    action. The action requires only (3) points.

    10 * 45 + 20 = 470 points

    So the method check_response has to return a False, because there is no logical mistake in the response.
    """

    def test_enough_points(self):
        response = {'type': 'putUnderQuarantine', 'city': 'Accra', 'rounds': 1}
        self.assertFalse(agent.check_response(response, game_json))

    """
    This test serves to check whether it is possible to execute an action for 0 laps. Because it is not logical to 
    quarantine a city for 0 laps.
    """

    def test_zero_rounds(self):
        response = {'type': 'putUnderQuarantine', 'city': 'Accra', 'rounds': 0}
        self.assertTrue(agent.check_response(response, game_json))

    """
    This method tries to quarantine a city. To do this, the action "putUnderQurantine" should be executed. Since a city 
    cannot be quarantined twice, the system checks if the city already has an event that indicates that the city is 
    quarantined.
    """

    def test_put_under_putUnderQuarantine(self):
        response = {'type': 'putUnderQuarantine', 'city': 'New York City', 'rounds': 2}
        self.assertTrue(agent.check_response(response, game_json))

    """
    This test tries to perform an action "closeAirport" which will close an airport.
    The method "check_response" must return false, because there is no logical error in this scenario.
    """

    def test_close_airport(self):
        response = {'type': 'closeAirport', 'city': 'Abuja', 'rounds': 2}
        self.assertFalse(agent.check_response(response, game_json))

    """
    This test tries to perform an action "closeAirport" which will close an airport.
    The method "check_response" must return true, because there is a logical error in this scenario. The airport is 
    already closed.
    """

    def test_close_closed_airport(self):
        response = {'type': 'closeAirport', 'city': 'New York City', 'rounds': 2}
        self.assertTrue(agent.check_response(response, game_json))

    """
    This test attempts to execute action "exertInfluence". Since this action has not yet been executed in the city where 
    the action is to be executed, the method "check_response" must return a false.
    """

    def test_wrong_exert_influence(self):
        response = {'type': 'exertInfluence', 'city': 'Anchorage', 'rounds': 2}
        self.assertTrue(agent.check_response(response, game_json))

    """
    This test attempts to execute action "exertInfluence". Since this action has already been executed in the city where 
    the action is to be executed, the method "check_response" must return a true.
    """

    def test_exert_influence(self):
        response = {'type': 'exertInfluence', 'city': 'Abuja', 'rounds': 2}
        self.assertFalse(agent.check_response(response, game_json))

    """
    This test attempts to execute action "callElections". Since this action has already been executed in the city where 
    the action is to be executed, the method "check_response" must return a true.
    """

    def test_wrong_call_elections(self):
        response = {'type': 'callElections', 'city': 'Abuja', 'rounds': 2}
        self.assertTrue(agent.check_response(response, game_json))

    """
    This test attempts to execute action "callElections". Since this action has not yet been executed in the city where 
    the action is to be executed, the method "check_response" must return a false.
    """

    def test_call_elections(self):
        response = {'type': 'callElections', 'city': 'Accra', 'rounds': 2}
        self.assertFalse(agent.check_response(response, game_json))

    """
    This test attempts to execute action "applyHygienicMeasures". Since this action has not yet been executed in the 
    city where the action is to be executed, the method "check_response" must return a false.
    """

    def test_apply_hygienic_measures(self):
        response = {'type': 'applyHygienicMeasures', 'city': 'Abuja', 'rounds': 2}
        self.assertFalse(agent.check_response(response, game_json))

    """
    This test attempts to execute action "applyHygienicMeasures". Since this action has already been executed in the 
    city where the action is to be executed, the method "check_response" must return a true.
    """

    def test_wrong_apply_hygienic_measures(self):
        response = {'type': 'applyHygienicMeasures', 'city': 'Portland', 'rounds': 2}
        self.assertTrue(agent.check_response(response, game_json))

    """
    This test attempts to execute action "launchCampaign". Since this action has already been executed in the 
    city where the action is to be executed, the method "check_response" must return a true.
    """

    def test_wrong_launch_campaign(self):
        response = {'type': 'launchCampaign', 'city': 'Abuja', 'rounds': 2}
        self.assertTrue(agent.check_response(response, game_json))

    """
    This test attempts to execute action "launchCampaign". Since this action has not yet been executed in the city where 
    the action is to be executed, the method "check_response" must return a false.
    """

    def test_launch_campaign(self):
        response = {'type': 'launchCampaign', 'city': 'New York City', 'rounds': 2}
        self.assertFalse(agent.check_response(response, game_json))

    """
    This test serves to check whether a disease exists globally. To do this, the type of event (pathogenEncountered) and
    the name of the disease are required. If the disease exists, the value true should be returned.
    """

    def test_existing_global_pathogen(self):
        pathogen_name = "Admiral Trips"
        type = "pathogenEncountered"
        self.assertTrue(agent.find_global_pathogen(game_json, pathogen_name, type))

    """
    This test serves to check whether a disease not exists globally. To do this, the type of event (pathogenEncountered) 
    and the name of the disease are required. If the disease not exists, the value false should be returned.
    """

    def test_not_existing_global_pathogen(self):
        pathogen_name = "Neurodermantotitis"
        type = "pathogenEncountered"
        self.assertFalse(agent.find_global_pathogen(game_json, pathogen_name, type))

    """
    The method "find_event_in_city", is used to check whether an action has already been executed in a city. The test 
    checks directly in three different cities whether the existing events are found there.
    """

    def test_existing_event_in_city(self):
        first_city = "Abuja"
        first_event = "campaignLaunched"

        second_city = "Albuquerque"
        second_event = "outbreak"

        third_city = "Portland"
        third_event = "hygienicMeasuresApplied"

        self.assertTrue(agent.find_event_in_city(game_json, first_city, first_event))
        self.assertTrue(agent.find_event_in_city(game_json, second_city, second_event))
        self.assertTrue(agent.find_event_in_city(game_json, third_city, third_event))

    """
    The method "find_event_in_city", is used to check whether an action has already been executed in a city. The test 
    checks directly in three different cities whether the non-existent events are found. Since the events do not exist, 
    a false should be returned.
    """

    def test_not_existing_event_in_city(self):
        first_city = "Abuja"
        first_event = "worldPiece#"

        second_city = "Albuquerque"
        second_event = "moneyRain"

        third_city = "Portland"
        third_event = "taxReduction"

        self.assertFalse(agent.find_event_in_city(game_json, first_city, first_event))
        self.assertFalse(agent.find_event_in_city(game_json, second_city, second_event))
        self.assertFalse(agent.find_event_in_city(game_json, third_city, third_event))

    """
    There are two global events, one for vaccines and one for drugs. While these things are being developed, they are 
    not yet available. The test ensures that this is detected and therefore no distribution requests are sent out while 
    it is still inDevelopment.
    The test should return True if it is still in development.
    """

    def test_find_existing_in_develop(self):
        first_pathogen_name = "Phagum vidiianum"
        first_type = "vaccine"

        second_pathogen_name = "Admiral Trips"
        second_type = "medication"

        self.assertTrue(agent.find_develop(game_json, first_pathogen_name, first_type))
        self.assertTrue(agent.find_develop(game_json, second_pathogen_name, second_type))

    """
    This test checks whether the "find_develop" method finds development for pathogens that do not exist. Since there 
    is a logical error, the return value should be False.
    """

    def test_find_not_existing_in_develop(self):
        first_pathogen_name = "moneyRain"
        first_type = "vaccine"

        second_pathogen_name = "texReduction"
        second_type = "medication"

        self.assertFalse(agent.find_develop(game_json, first_pathogen_name, first_type))
        self.assertFalse(agent.find_develop(game_json, second_pathogen_name, second_type))

    """
    As soon as a drug or vaccine is available, it is globally advertised as "Available". The method checks whether this 
    is also found. Since this is logically correct, the method should return False.
    """

    def test_find_existing_available(self):
        first_pathogen_name = "Procrastinalgia"
        first_type = "vaccine"

        second_pathogen_name = "Methanobrevibacter colferi"
        second_type = "medication"

        self.assertFalse(agent.find_develop(game_json, first_pathogen_name, first_type))
        self.assertFalse(agent.find_develop(game_json, second_pathogen_name, second_type))

    """
    To be able to distribute a medicine or vaccine, it must be available globally and the desired city must also be 
    infected with the disease for which the vaccine / medicine was developed. Since the medicine and vaccine are 
    available, it can be distributed in the city. Return value should therefore be False.
    """

    def test_find_correct_deployment(self):
        pathogen_name = "Methanobrevibacter colferi"
        city = "Abuja"

        first_type = "vaccine"
        second_type = "medication"

        self.assertFalse(agent.find_deployment(game_json, pathogen_name, city, first_type))
        self.assertFalse(agent.find_deployment(game_json, pathogen_name, city, second_type))

    """
    After a defined iteration step, the models should be saved. If this does not yet exist, a folder "max" is created. 
    In this folder the models are saved and a folder with the current iteration step is created. If "max" already 
    exists, the content will be overwritten, but a new folder with the current iteration step will be created. Before 
    saving, it is checked how many iteration folders there are. After saving, the same is asked again and if there is a 
    higher number, it is also checked if there is content in it. If everything is correct, a variable is set to True, 
    which is checked at the end of the test.
    """

    def test_save_model(self):
        saved = False
        iteration_counter = 0
        check_counter = 0
        if path.exists("pytorch_models"):
            iteration_counter = self.get_hightest_model()
            agent.save(iteration_counter + 1)
            check_counter = self.get_hightest_model()
            if iteration_counter < check_counter:
                if os.path.getsize("pytorch_models/" + str(check_counter)) > 0:
                    saved = True
        self.assertTrue(saved)

    """
    Help method to reduce the code. The method is used to look in the file tree, in the folder pytorch_models, to see 
    which is the highest iteration step.
    """

    def get_hightest_model(self):
        iteration_counter = 0
        for dic in os.listdir("pytorch_models"):
            if dic.isnumeric():
                if iteration_counter < int(dic):
                    iteration_counter = int(dic)
        return iteration_counter

    """
    To check whether the models are also loaded, models are first saved so that there is something to load.
    First of all it is checked whether the folder "pytorch_models" contains the folder "max", in which the most recent 
    models are located. If they are available, they are copied into the folder "help" for later comparison. Then the 
    models are loaded and saved again directly afterwards. Since no training was running, the data should be the same. 
    This is checked with the library filecmp.
    If the folder "max" is not available, the folder with the highest iteration value is taken.
    """

    def test_load_models(self):
        agent.save(self.get_hightest_model())
        if path.exists("pytorch_models/max"):
            copy_tree("pytorch_models/max", "pytorch_models/help")
            agent.load()
            agent.save(self.get_hightest_model() + 1)
            test = filecmp.dircmp("pytorch_models/max", "pytorch_models/help")
            test_wrong = filecmp.dircmp("pytorch_models/max", "pytorch_test_models")
            self.assertTrue(test.diff_files == [])
            self.assertFalse(test_wrong.diff_files == [])
        else:
            copy_tree("pytorch_models/" + str(self.get_hightest_model()), "pytorch_models/help")
            agent.load("pytorch_models/" + str(self.get_hightest_model()))
            agent.save(self.get_hightest_model() + 1)
            test = filecmp.dircmp("pytorch_models/" + str(self.get_hightest_model()), "pytorch_models/help")
            test_wrong = filecmp.dircmp("pytorch_models/" + str(self.get_hightest_model()), "pytorch_test_models")
            self.assertTrue(test.diff_files == [])
            self.assertFalse(test_wrong.diff_files == [])

    """
    The act method from the TorchAgent, is used to have the network calculate any possible decisions for the cities and 
    diseases and then summarize them in a list. This list must be sorted so that the most important action is at the 
    top. The test is used to check that the list is sorted correctly.
    As soon as a value with a higher index has a greater number than its predecessor, an error occurs. Otherwise the 
    test should be completed with False. Translated with www.DeepL.com/Translator (free version)
    """

    def test_act(self):
        state = StateGenerator(game_json)
        result_list = agent.act(state)
        check = False
        lowest = 1
        for x in result_list:
            if lowest >= x[1]:
                lowest = x[1]
            else:
                check = True
                break
        self.assertFalse(check)

    """
    The method get_disease_action receives a list of diseases. The possible actions for the diseases are calculated from
    these diseases. The test checks that only actions for the diseases that actually exist are created.
    As soon as an action occurs for a disease that does not exist, error is set to True. Finally, it checks for False.
    """

    def test_get_disease_action(self):
        diseases = GameJson.diseases
        disease_names = ["Endoictus", "Moricillus ☠", "Admiral Trips"]
        result = agent.get_disease_actions(diseases, game_json['round'])
        error = False
        previous = -1
        for disease in result:
            json_help = json.loads(disease[0])
            if json_help['pathogen'] not in disease_names:
                error = True
            if disease[1] < previous:
                error = True
            previous = disease[1]
        self.assertFalse(error)

    """
    The method "get_city_action" returns a list. This list contains all possible actions for the cities that have been 
    calculated by the network. These are sorted and should of course only contain actions for the cities that exist. 
    Check by the GameJson, which reflects a shortened version of the Json from the ic20.
    Checks for false, because the cities should be correct and a sorted list should be available.
    """

    def test_get_city_action(self):
        cities = GameJson.cities
        diseases = GameJson.diseases
        result_list = agent.get_actions(cities, diseases, game_json['round'])
        error = False
        previous = -1
        for result in result_list:
            to_json = json.loads(result[0])
            if to_json['type'] != "endRound":
                if to_json['city'] not in GameJson.city_names:
                    error = True
                if result[1] < previous:
                    error = True
                previous = result[1]
        self.assertFalse(error)

    # TODO: Need to implement

    def test_train(self):
        agent.train()

    def test_update_reward(self):
        reward = 100
        agent.update_reward(reward)


if __name__ == '__main__':
    unittest.main()
