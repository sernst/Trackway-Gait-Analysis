import unittest
from unittest import mock

from tracksim import paths
from tracksim import system
from tracksim import configs

class test_configs(unittest.TestCase):

    def setUp(self):
        """
        """
        pass

    def test_load_missing(self):
        """
        """
        path = paths.project('does_not_exist.fake')
        mm_end = mock.MagicMock(name='end')
        system.end = mm_end

        configs.load('trial', path)
        mm_end.assert_called_once_with(1)

    def test_load_invalid(self):
        """
        """
        path = paths.project('tests', 'resources', 'invalid.json')
        mm_end = mock.MagicMock(name='end')
        system.end = mm_end

        configs.load('trial', path)
        mm_end.assert_called_once_with(1)

    def test_activity_to_support(self):
        """

        :return:
        """

        duty_cycle = 0.75
        activity_phases = [0, 0.5, -1.0, -0.5]

        support_phases = configs.activity_to_support_phases(
            activity_phases,
            duty_cycle
        )

        print('A->S:', support_phases)
        self.assertEqual(support_phases[0], -0.25)
        self.assertEqual(support_phases[1], 0.25)
        self.assertEqual(support_phases[2], -1.25)
        self.assertEqual(support_phases[3], -0.75)

    def test_support_to_activity(self):
        """

        :return:
        """

        duty_cycle = 0.75
        support_phases = [-0.25, 0.25, -1.25, -0.75]
        # activity_phases = [0, 0.5, -1.0, -0.5]

        activity_phases = configs.support_to_activity_phases(
            support_phases,
            duty_cycle
        )

        print('S->A:', activity_phases)
        self.assertEqual(activity_phases[0], 0)
        self.assertEqual(activity_phases[1], 0.5)
        self.assertEqual(activity_phases[2], -1.0)
        self.assertEqual(activity_phases[3], -0.5)


################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_configs)
    unittest.TextTestRunner(verbosity=2).run(suite)




