import unittest

from tracksim import paths
from tracksim import trackway

class test_trackway(unittest.TestCase):

    def setUp(self):
        """
        """
        pass

    def test_load_positions_file(self):
        """
        """

        path = paths.project('test_resources', 'test_data.csv')
        positions = trackway.load_positions_file(path)
        self.assertEqual(len(positions.left_manus), 18)
        self.assertEqual(len(positions.right_manus), 20)
        self.assertEqual(len(positions.left_pes), 21)
        self.assertEqual(len(positions.right_pes), 21)

        result = positions.left_pes[0].echo()
        self.assertIsNotNone(result)

    def test_load_pes_only_file(self):
        """
        """

        path = paths.project('test_resources', 'pes_only_test_data.csv')

        positions = trackway.load_positions_file(path)
        self.assertEqual(len(positions.left_manus), 4)
        self.assertEqual(len(positions.right_manus), 5)
        self.assertEqual(len(positions.left_pes), 4)
        self.assertEqual(len(positions.right_pes), 5)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_trackway)
    unittest.TextTestRunner(verbosity=2).run(suite)



