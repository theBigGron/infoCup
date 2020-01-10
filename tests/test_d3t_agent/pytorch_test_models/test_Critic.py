import unittest

from common.d3t_agent.Critic import Critic


class CriticTest(unittest.TestCase):
    """
    The test serves to validate the initialization of the critic. It is created with the given parameters and then
    checked for correct values.
    """

    def test_init(self):
        state_dim = 10
        action_dim = 10
        critic = Critic(state_dim, action_dim)
        self.assertTrue(critic.layer_1.in_features == state_dim + action_dim)
        self.assertTrue(critic.layer_3.in_features == 10)
        self.assertTrue(critic.layer_4.out_features == 1)
        self.assertTrue(critic.layer_5.in_features == state_dim + action_dim)
        self.assertTrue(critic.layer_7.in_features == 10)
        self.assertTrue(critic.layer_8.out_features == 1)

    """
    The test serves to validate the initialization of the critic. It is created with the given parameters and then 
    checked for correct values.
    """

    def test_init_2(self):
        state_dim = 3
        action_dim = 8
        critic = Critic(state_dim, action_dim)
        self.assertTrue(critic.layer_1.in_features == state_dim + action_dim)
        self.assertTrue(critic.layer_3.in_features == 10)
        self.assertTrue(critic.layer_4.out_features == 1)
        self.assertTrue(critic.layer_5.in_features == state_dim + action_dim)
        self.assertTrue(critic.layer_7.in_features == 10)
        self.assertTrue(critic.layer_8.out_features == 1)


if __name__ == '__main__':
    unittest.main()
