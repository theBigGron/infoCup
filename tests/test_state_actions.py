import json
from unittest import TestCase

import unittest

import numpy as np

from common.data_processing.state_actions import Actions, ActionInfo, ENUM_ACTIONS
from tests.data_for_tests.GameJson import diseases


class TestStateActions(unittest.TestCase):

    def test_get_enum_by_index(self):
        self.assertEqual('{"type":"endRound"}', ENUM_ACTIONS[0])
        self.assertEqual('{{"type": "developMedication", "pathogen": "{pathogen}" }}', ENUM_ACTIONS[10])
        self.assertEqual('{{"type": "developMedication", "pathogen": "{pathogen}" }}',
                         ENUM_ACTIONS[len(ENUM_ACTIONS)-1])

    def test_init_city_actions(self):
        q = np.asarray([x / 20 for x in reversed(range(0, 17, 1))])
        q.reshape(-1, 1)
        city = "Oldenburg"
        actions = Actions(city, diseases[0]["name"], q)
        for x in actions.action_list:
            print(x)
        self.assertTrue(actions.action_list[0][1] >= actions.action_list[-1][1])
        self.assertEqual(len(actions.action_list), 11)

    def test_sorted_actions(self):
        inf1 = Actions(
                        city_name="Oldenburg",
                        pathogen="Sars",
                        state=np.array([x for x in range(0, 3)]).reshape(-1, 1),
                        action_out=np.array([x for x in range(0, 12)]).reshape(-1, 1),
                        )

        for x in range(1, len(inf1.action_list)):
            a1 = inf1.action_list[x-1]
            a2 = inf1.action_list[x]
            self.assertGreaterEqual(a1, a1)
            self.assertGreater(a1, a2)
            self.assertLess(a2, a1)


class TestActionInfo(TestCase):
    def test_compare_info(self):
        inf1 = ActionInfo("None", "None", None, None, 0.0, "None", 1, )
        inf2 = ActionInfo("None", "None", None, None, 0.1, "None", 1,)
        inf3 = \
            ActionInfo("None", "None", None, None, 0.1, "None", 1, )

        self.assertTrue(inf1 < inf2)
        self.assertFalse(inf2 < inf1)
        self.assertFalse(inf2 < inf3)

    def test_right_values(self):
        inf1 = ActionInfo('Accra', None, None, None, 0, ENUM_ACTIONS[1], 45, None)
        # Direct comparison does not work due to pythons handling of dicts.
        self.assertEqual(json.loads('{"type": "putUnderQuarantine", "city": "Accra", "rounds": 45}'),
                         json.loads(inf1.server_message))
