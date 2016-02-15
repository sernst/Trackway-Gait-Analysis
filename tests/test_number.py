# test_number.py [UNIT TEST]
# (C) 2015
# Scott Ernst

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from tracksim import number

class test_number(unittest.TestCase):

    def test_roundingIssue(self):
        """ doc... """
        x1 = number.ValueUncertainty(1.3125, 0.010050373127401788)
        y1 = number.ValueUncertainty(0.2, 0.010050373127401788)
        x2 = number.ValueUncertainty(1.3125, 0.08749999999999997)
        y2 = number.ValueUncertainty(0.0, 0.010050373127401788)

        a = x2 - x1
        a_squared = a ** 2
        b = y2 - y1
        b_squared = b ** 2
        summed = a_squared + b_squared

        result = summed ** 0.5

        print(result)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_number)
    unittest.TextTestRunner(verbosity=2).run(suite)



