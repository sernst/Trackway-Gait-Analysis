import os
import unittest

from tracksim import paths
from tracksim import system

MY_PATH = os.path.abspath(__file__)
MY_DIRECTORY = os.path.abspath(os.path.dirname(MY_PATH))


class test_tracksim(unittest.TestCase):
    """
        Unit testing for the top-level tracksim module
    """

    def test_project_path(self):
        """
            Tests making project paths
        """

        # Without arguments
        project_root_path = os.path.abspath(os.path.join(
            MY_DIRECTORY, '..', '..'
        ))
        self.assertEqual(project_root_path, paths.project())

        # With arguments
        self.assertEqual(
            MY_PATH,
            paths.project('tracksim', 'tests', 'test_tracksim.py')
        )

    def test_resource_path(self):
        """
            Tests making project paths
        """

        # Without arguments
        resources_root_path = os.path.abspath(os.path.join(
            MY_DIRECTORY, '..', '..', 'resources'
        ))
        self.assertEqual(resources_root_path, paths.resource())

    def test_logging(self):
        """
        """

        system.log('This is a test')

        system.log([
            '1',
            ['2', '3',
             ['4', '5', '6']
             ]
        ])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_tracksim)
    unittest.TextTestRunner(verbosity=2).run(suite)



