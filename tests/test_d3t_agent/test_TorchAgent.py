import filecmp
import hashlib
import unittest
import os.path
import json
from distutils.dir_util import copy_tree

from common.d3t_agent.TorchAgent import TorchAgent
from common.data_processing.state_extractor import GameState
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
        if not path.exists("pytorch_models"):
            os.makedirs("pytorch_models")
        iteration_counter = self.get_hightest_model()
        agent.save("pytorch_models/" + str(iteration_counter + 1))
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
        agent.load("pytorch_models/1")
        if not path.exists("pytorch_models"):
            os.makedirs("pytorch_models")
        agent.save("pytorch_models/" + str(self.get_hightest_model() + 1))
        hash_md5 = hashlib.md5()
        with open("pytorch_models/1/actor.pth.tar", "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        hash_md5_2 = hashlib.md5()

        with open("max/actor.pth.tar", "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5_2.update(chunk)

        print(hash_md5.hexdigest())
        print(hash_md5_2.hexdigest())
    """
    The act method from the TorchAgent, is used to have the network calculate any possible decisions for the cities and 
    diseases and then summarize them in a list. This list must be sorted so that the most important action is at the 
    top. The test is used to check that the list is sorted correctly.
    As soon as a value with a higher index has a greater number than its predecessor, an error occurs. Otherwise the 
    test should be completed with False. Translated with www.DeepL.com/Translator (free version)
    """

    def test_act(self):
        state = GameState(game_json)
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
        result_list = agent._get_actions(cities, diseases, game_json['round'])
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
