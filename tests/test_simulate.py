from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import tracksim
from tracksim.group import simulate as simulate_group
from tracksim.trial import simulate as simulate_trial


class test_simulate(unittest.TestCase):

    def test_validation(self):
        """

        :return:
        """

        configs_path = tracksim.make_project_path(
                'tests', 'resources', 'phase_validation.json')
        simulate_trial.run(configs_path)

    def test_data_file_trial(self):
        """

        :return:
        """

        configs_path = tracksim.make_project_path(
                'tests', 'resources', 'test_trial_5.json')
        simulate_trial.run(configs_path)

    def test_run_group(self):
        """
            Carries out a test run of a complete simulation trial using
            generated data
        """

        configs_path = tracksim.make_project_path(
                'tests', 'resources', 'test_group.json')
        simulate_group.run(configs_path)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_simulate)
    unittest.TextTestRunner(verbosity=2).run(suite)



