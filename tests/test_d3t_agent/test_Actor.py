import unittest

from common.d3t_agent.Actor import Actor

"""
This class contains the tests for the class Actor.
"""

class ActorTest(unittest.TestCase):
    """
    The test serves to validate the initialization of the actor. It is created with the given parameters and then
    checked for correct values.
    """

    def test_init(self):
        state_dim = 2
        action_dim = 7
        max_action = 9
        test_actor = Actor(state_dim, action_dim, max_action)
        self.assertTrue(test_actor.layer_1.in_features == state_dim)
        self.assertTrue(test_actor.layer_5.out_features == action_dim)
        self.assertTrue(test_actor.max_action == max_action)

    """
    The test serves to validate the initialization of the actor. It is created with the given parameters and then 
    checked for correct values.
    """

    def test_init_2(self):
        state_dim = 3
        action_dim = 1
        max_action = 3
        test_actor = Actor(state_dim, action_dim, max_action)
        self.assertTrue(test_actor.layer_1.in_features == state_dim)
        self.assertTrue(test_actor.layer_5.out_features == action_dim)
        self.assertTrue(test_actor.max_action == max_action)
        self.assertFalse(test_actor.layer_1.in_features == state_dim - 1)


if __name__ == '__main__':
    unittest.main()