
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import tracksim
from tracksim import svg
from tracksim.svg import draw
from tracksim import generate

class test_svg(unittest.TestCase):

    def test_simple_write(self):
        """

        :return:
        """

        writer = svg.SvgWriter()

        writer.draw_circle(10, 10, 5, 'test')
        writer.add_style_definition('.test', {
            'fill': '#999',
            'stroke': '#333',
            'stroke-width': '1px'
        })

        result = writer.dumps()
        print(result)

    def test_draw_trackway_positions(self):
        """

        :return:
        """

        drawer = svg.SvgWriter()

        phases = tracksim.LimbProperty().assign(0.0, 0.5, 0.6, 0.1)

        trackway = generate.trackway_data(
            count=12,
            step_size=0.75,
            limb_offsets=phases,
            limb_phases=phases,
            lateral_displacement=0.1)

        draw.trackway_positions(
            limb_positions=trackway.limb_positions,
            drawer=drawer)

        result = drawer.dumps()
        print(result)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_svg)
    unittest.TextTestRunner(verbosity=2).run(suite)



