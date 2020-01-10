import unittest
import json
import pprint

from common.data_processing.state_extractor import StateGenerator
from tests.GameJson import game_json
from tests.GameJson import game_json2

class TestExtractor(unittest.TestCase):
    def setUp(self):
        # with open(file="GameJson2.py", mode='w', encoding='utf-8') as f:
        #     pp = pprint.PrettyPrinter(indent=4, stream=f)
        #     with open(file="test.json", mode='r', encoding='utf-8') as f:
        #         data = json.load(f)
        #         self.sg = StateGenerator(data)
        #         pp.pprint(data)

        self.sg1 = StateGenerator(game_json)
        self.sg2 = StateGenerator(game_json2)


    def tearDown(self):
        pass

    def test_meta_data(self):
        self.assertEqual(self.sg2.round, 1)
        self.assertEqual(self.sg2.points, 40)

    def test_build_norm_disease_info_list(self):
        self.sg2.build_norm_disease_info_list()
        disease_info_list_of_dicts = []
        disease_info_dict = {
            'id': 0,
            'name': 'Admiral Trips',
            'vaccine_available_or_in_development': 0,
            'medication_available_or_in_development': 0,
            'duration': 0.25,
            'lethality': 1,
            'infectivity': 1,
            'mobility': 0.75,
            'world_prevalence': 0.0003014393730061041
        }
        disease_info_list_of_dicts.append(disease_info_dict)
        disease_info_dict = {
            'id': 1,
            'name': 'Neurodermantotitis',
            'vaccine_available_or_in_development': 0,
            'medication_available_or_in_development': 0,
            'duration': 0.5,
            'lethality': 0.5,
            'infectivity': 0.75,
            'mobility': 0.5,
            'world_prevalence': 0.0020452925878966803
        }
        disease_info_list_of_dicts.append(disease_info_dict)
        self.assertEqual(self.sg2.disease_info_list_of_dicts, disease_info_list_of_dicts)

    def test_build_city_info_list(self):
        self.sg2.build_city_info_list()
        city_info_dict = {
            'city_name': 'Abuja',
            # Norm the population in regard to former calculated world_population
            'population': 0.003635781911257835,
            # Count the connections and norm them by dividing through MAX_AMOUNT_OF_CONNECTIONS
            'amount_connections': 0.25,
            # This calculates the sum of the populations of the connected cities
            # and norms it by dividing with world_population
            'connected_city_population':0.014492887749530323,
            # These statements grab the value with given key from SYM_VALUE_NORM_NUMBER_DICT in order to
            # map --, ..., ++ to 0, ..., 1
            'economy': 0.5,
            'government': 0.25,
            'hygiene': 0.25,
            'awareness': 0.25,
            'anti-vaccinationism': 0
            # 'disease__prevalence':
        }
        self.assertEqual(self.sg2.city_info_list_of_dicts[0], city_info_dict)

    def test_world_population(self):
        self.assertEqual(self.sg2.world_population, 756371)
    # def test_empty_post_req(self):
    #    response = self.app.post("", follow_redirects=True)
    #    self.assertEqual(response.status, "200 OK")
    #    self.assertEqual(str(response.data), "b''")

    # def test_seed_1(self):
    #    with open(file="test.json", mode='r', encoding='utf-8') as f:
    #        data = json.load(f)
    #        response = self.app.post("/", data=json.dumps(data), follow_redirects=True, content_type='application/json')
    #        self.assertEqual(response.status, "200 OK")
    #        self.assertEqual(response.json, {"type": "endRound"})

    def test_is_available_or_in_development_for_disease(self):
        self.sg1.build_norm_disease_info_list()
        disease_info_dict = {
            'duration': 0.25,
            'id': 2,
            'infectivity': 1,
            'lethality': 1,
            'medication_available_or_in_development': 0.625,
            'mobility': 0.75,
            'name': 'Admiral Trips',
            'vaccine_available_or_in_development': 0,
            'world_prevalence': 0.0
        }
        self.assertEqual(self.sg1.disease_info_list_of_dicts[2], disease_info_dict)


if __name__ == '__main__':
    unittest.main()
