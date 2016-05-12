import unittest

from tracksim import paths
from tracksim import system
from tracksim.group import simulate as simulate_group
from tracksim.trial import simulate as simulate_trial


class test_simulate(unittest.TestCase):

    def test_validation(self):
        """

        :return:
        """

        configs_path = paths.project(
                'test_resources', 'phase_validation.json'
        )
        simulate_trial.run(configs_path)

    def test_run_group(self):
        """
            Carries out a test run of a complete simulation trial using
            generated data
        """

        configs_path = paths.project(
                'test_resources', 'unit_test_group.json'
        )
        simulate_group.run(configs_path)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_simulate)
    unittest.TextTestRunner(verbosity=2).run(suite)



