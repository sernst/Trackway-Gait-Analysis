from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest

import tracksim

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
        project_root_path = os.path.abspath(os.path.join(MY_DIRECTORY, '..'))
        self.assertEqual(project_root_path, tracksim.make_project_path())

        # With arguments
        self.assertEqual(
                MY_PATH,
                tracksim.make_project_path('tests', 'test_tracksim.py'))

    def test_resource_path(self):
        """
            Tests making project paths
        """

        # Without arguments
        resources_root_path = os.path.abspath(os.path.join(
                MY_DIRECTORY, '..', 'resources' ))
        self.assertEqual(resources_root_path, tracksim.make_resource_path())

    def test_logging(self):
        """
        """

        tracksim.log('This is a test')

        tracksim.log([
            '1',
            ['2', '3',
             ['4', '5', '6']
             ]
        ])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_tracksim)
    unittest.TextTestRunner(verbosity=2).run(suite)



