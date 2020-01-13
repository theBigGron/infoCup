import unittest
import json
import pprint

from common.data_processing.state_extractor import GameState
from common.data_processing.utils import eval_disease_prevalence
from tests.data_for_tests import GameJson
from tests.data_for_tests.GameJson import game_json
from tests.data_for_tests.GameJson import game_json2

class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.sg1 = GameState(game_json)
        self.sg2 = GameState(game_json2)
        self.game_state = GameState(GameJson.game_json)


    def tearDown(self):
        pass

    def test_meta_data(self):
        self.assertEqual(1, self.sg2.round)
        self.assertEqual(40, self.sg2.points)

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
        self.assertEqual(disease_info_list_of_dicts, self.sg2.disease_info_list_of_dicts)

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
            'disease_prevalence': {},
            # These statements grab the value with given key from SYM_VALUE_NORM_NUMBER_DICT in order to
            # map --, ..., ++ to 0, ..., 1
            'economy': 0.5,
            'government': 0.25,
            'hygiene': 0.25,
            'awareness': 0.25,
            'anti-vaccinationism': 0
            # 'disease__prevalence':
        }
        self.assertEqual(city_info_dict, self.sg2.city_info_list_of_dicts[0])

    def test_world_population(self):
        self.assertEqual(756371, self.sg2.world_population)
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

    def test_eval_disease_prevalence(self):
        data = GameJson.city_obj[0]
        diseases_with_prevalence = eval_disease_prevalence(data)
        self.assertTrue(diseases_with_prevalence["Geranitis"] == 0.6)
        self.assertTrue(diseases_with_prevalence["Neurodermantotitis"] == 0.1)

    def test_find_event_in_city(self):

        self.assertTrue(self.game_state.event_exists_in_city('New York City', "quarantine"))
        self.assertFalse(self.game_state.event_exists_in_city('Abuja', "quarantine"))
        self.assertTrue(self.game_state.event_exists_in_city('New York City', "outbreak"))
        self.assertTrue(self.game_state.event_exists_in_city('New York City', "airportClosed"))
        self.assertFalse(self.game_state.event_exists_in_city('Abuja', "airportClosed"))

    def test_find_develop(self):
        self.assertTrue(self.game_state.aid_in_development(pathogen_name="Phagum vidiianum", aid_type="vaccine"))
        self.assertTrue(self.game_state.aid_in_development(pathogen_name="Admiral Trips", aid_type="medication"))
        self.assertFalse(self.game_state.aid_in_development(pathogen_name="asd", aid_type="vaccine"))
        self.assertFalse(self.game_state.aid_in_development(pathogen_name="Adips", aid_type="medication"))

    def test_find_developed(self):
        self.assertTrue(
            self.game_state.aid_developed(pathogen_name="Methanobrevibacter colferi", aid_type="medication"))
        self.assertTrue(
            self.game_state.aid_developed(pathogen_name="Procrastinalgia", aid_type="vaccine"))
        self.assertFalse(
            self.game_state.aid_developed(pathogen_name="asfafasfi", aid_type="medication"))
        self.assertFalse(
            self.game_state.aid_developed(pathogen_name="jghd", aid_type="vaccine"))

    def test_lock_down_over(self):
        self.assertTrue(
            self.game_state.lock_down_over(city_name="New York City", event_type="quarantine", round_=10))
        self.assertFalse(
            self.game_state.lock_down_over(city_name="New York City", event_type="quarantine", round_=9))
        self.assertFalse(
            self.game_state.lock_down_over(city_name="New York City", event_type="quarantine", round_=6))
        self.assertTrue(
            self.game_state.lock_down_over(city_name="Abuja", event_type="quarantine", round_=10))
        self.assertTrue(
            self.game_state.lock_down_over(city_name="New York City", event_type="airportClosed", round_=8))
        self.assertFalse(
            self.game_state.lock_down_over(city_name="New York City", event_type="airportClosed", round_=7))
        self.assertFalse(
            self.game_state.lock_down_over(city_name="New York City", event_type="airportClosed", round_=3))
        self.assertTrue(
            self.game_state.lock_down_over(city_name="Abuja", event_type="airportClosed", round_=10))


if __name__ == '__main__':
    unittest.main()
