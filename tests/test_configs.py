import unittest
from unittest import mock

import tracksim
from tracksim import configs

class test_configs(unittest.TestCase):

    def setUp(self):
        """
        """
        pass

    def test_load_missing(self):
        """
        """
        path = tracksim.make_project_path('does_not_exist.fake')
        mm_end = mock.MagicMock(name='end')
        tracksim.end = mm_end

        configs.load(path)
        mm_end.assert_called_once_with(1)

    def test_load_invalid(self):
        """
        """
        path = tracksim.make_project_path('tests', 'resources', 'invalid.json')
        mm_end = mock.MagicMock(name='end')
        tracksim.end = mm_end

        configs.load(path)
        mm_end.assert_called_once_with(1)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_configs)
    unittest.TextTestRunner(verbosity=2).run(suite)




