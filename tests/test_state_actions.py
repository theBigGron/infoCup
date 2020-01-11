import unittest

import numpy as np

from common.data_processing.state_actions import Actions, get_number_of_actions
from tests.data_for_tests.GameJson import diseases


class TestStateActions(unittest.TestCase):
    def test_init_city_actions(self):
        q = np.asarray([x/20 for x in reversed(range(0, 17, 1))])
        q.reshape(-1, 1)
        city = "Oldenburg"
        actions = Actions(city, diseases[0]["name"], q)
        for x in actions.action_list:
            print(x)
        self.assertTrue(actions.action_list[0][1] >= actions.action_list[-1][1])
        self.assertEqual(len(actions.action_list), 11)

    def test_get_number_of_actions(self):
        self.assertEqual(get_number_of_actions(), 12)
