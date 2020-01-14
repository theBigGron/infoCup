import unittest

import numpy as np

from common.d3t_agent.ReplayMemory import ReplayBuffer
from common.data_processing.state_actions import ActionInfo, ENUM_ACTIONS

replay = ReplayBuffer()

"""
This class contains the tests for the class ReplayMemory.
"""


class ReplayMemoryTest(unittest.TestCase):

    def test_add(self):
        added = False
        city_name = "Portland"
        pathogen_name = "Admiral Trips"
        state = np.array(
            [0.00000000e+00, 0.00000000e+00, 5.00000000e-01, 5.00000000e-01, 5.00000000e-01, 7.50000000e-01,
             1.03123996e-04])
        action_out = np.array([0.04215073, 0.03435021])
        activation = 0.3546438536937
        action = ENUM_ACTIONS[1]
        rounds_ = 5
        round_ = 25
        action_info = ActionInfo(city_name, pathogen_name, state, action_out, activation, action, rounds_, round_)
        replay.add(action_info)
        if len(replay.storage_buffer) > 0:
            added = True
        self.assertTrue(added)

    """
    The method "flush" cleared the attribute objects and storage in the replayMemory. This test add something to both 
    attributes and after that it called flush. After the flush, the attributes had the be empty. Only if the attributes 
    contains something before the flush-method is called and are empty after the flush was called, the error will be set 
    to false and the test are correct.
    """

    def test_flush(self):
        city_name = "New York City"
        pathogen_name = "Hexapox"
        state = np.array(
            [0.00000000e+00, 0.00000000e+00, 5.00000000e-01, 5.00000000e-01, 5.00000000e-01, 7.50000000e-01,
             1.03123996e-04])
        action_out = np.array([0.04215073, 0.03435021])
        activation = 0.3546438536937
        action = ENUM_ACTIONS[1]
        rounds_ = 5
        round_ = 25
        action_info = ActionInfo(city_name, pathogen_name, state, action_out, activation, action, rounds_, round_)
        replay.add(action_info)
        error = True
        if bool(replay.storage_buffer):
            replay.flush_buffer()
            if not bool(replay.storage_buffer):
                error = False
        self.assertFalse(error)

    # TODO Need to be implemented
    def test_sample(self):
        print("Without Function")

    def test_update_reward(self):
        print("Without Function")

    def test_save_buffer(self):
        print("Without Function")


if __name__ == '__main__':
    unittest.main()
