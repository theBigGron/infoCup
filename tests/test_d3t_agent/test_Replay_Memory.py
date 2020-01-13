import unittest

import numpy as np

from common.d3t_agent.ReplayMemory import ReplayBuffer

replay = ReplayBuffer()

"""
This class contains the tests for the class ReplayMemory.
"""


class ReplayMemoryTest(unittest.TestCase):

    def test_add(self):
        added = False
        state_old = np.array(
            [0.00000000e+00, 0.00000000e+00, 5.00000000e-01, 5.00000000e-01, 5.00000000e-01, 7.50000000e-01,
             1.03123996e-04])
        action = np.array([0.04215073, 0.03435021])
        object_name = "Hexapox"
        round_ = 1
        state_new = None
        reward = None
        replay.add(state_old, action, object_name, round_, state_new, reward)
        if len(replay.objects) > 0:
            added = True
        self.assertTrue(added)

    """
    The method "flush" cleared the attribute objects and storage in the replayMemory. This test add something to both 
    attributes and after that it called flush. After the flush, the attributes had the be empty. Only if the attributes 
    contains something before the flush-method is called and are empty after the flush was called, the error will be set 
    to false and the test are correct.
    """

    def test_flush(self):
        state_old = np.array(
            [0.00000000e+00, 0.00000000e+00, 5.00000000e-01, 5.00000000e-01, 5.00000000e-01, 7.50000000e-01,
             1.03123996e-04])
        action = np.array([0.04215073, 0.03435021])
        object_name = "Hexapox"
        round_ = 1
        state_new = None
        reward = None
        replay.add(state_old, action, object_name, round_, state_new, reward)
        replay.storage.append("test")
        error = True
        if bool(replay.storage):
            if bool(replay.objects):
                replay.flush_buffer()
                if not bool(replay.storage):
                    if not bool(replay.objects):
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
