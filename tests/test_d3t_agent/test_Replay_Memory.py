import unittest

import numpy as np

from common.d3t_agent.ReplayMemory import ReplayBuffer

replay = ReplayBuffer()


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


if __name__ == '__main__':
    unittest.main()
