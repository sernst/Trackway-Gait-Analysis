from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import tracksim
from tracksim import simulate

class test_simulate(unittest.TestCase):

    def test_validation(self):
        """

        :return:
        """

        configs_path = tracksim.make_project_path(
                'tests', 'resources', 'phase_validation.json')
        simulate.run(configs_path)

    def test_run(self):
        """
            Carries out a test run of a complete simulation trial using
            generated data
        """

        for i in range(5):
            configs_path = tracksim.make_project_path(
                    'tests', 'resources', 'test_trial_{}.json'.format(i + 1))
            simulate.run(configs_path)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_simulate)
    unittest.TextTestRunner(verbosity=2).run(suite)



