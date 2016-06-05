import unittest
import math

import measurement_stats as mstats
from tracksim.trackway import TrackPosition
from tracksim.trial.analyze import geometry

class TestGeometry(unittest.TestCase):

    def test_line_extension_horizontal(self):
        """
        """
        start = TrackPosition(
            mstats.ValueUncertainty(2, 0.1),
            mstats.ValueUncertainty(2, 0.1)
        )
        end = TrackPosition(
            mstats.ValueUncertainty(3, 0.1),
            mstats.ValueUncertainty(2, 0.1)
        )

        l = geometry.LineSegment2D(start, end)
        length = l.length.raw

        post_delta = 1.2
        l.post_extend_line(post_delta, replace=False)

        self.assertAlmostEqual(l.start.x.raw, start.x.raw)
        self.assertAlmostEqual(l.start.y.raw, start.y.raw)
        self.assertAlmostEqual(l.end.x.raw, end.x.raw + post_delta)
        self.assertAlmostEqual(l.end.y.raw, end.y.raw)
        self.assertAlmostEqual(length + post_delta, l.length.raw)

        pre_delta = 2.3
        l.pre_extend_line(pre_delta, replace=False)

        self.assertAlmostEqual(l.start.x.raw, start.x.raw - pre_delta)
        self.assertAlmostEqual(l.start.y.raw, start.y.raw)
        self.assertAlmostEqual(l.end.x.raw, end.x.raw + post_delta)
        self.assertAlmostEqual(l.end.y.raw, end.y.raw)
        self.assertAlmostEqual(length + post_delta + pre_delta, l.length.raw)

    def test_line_extension_vertical(self):
        """
        """
        start = TrackPosition(
            mstats.ValueUncertainty(2, 0.1),
            mstats.ValueUncertainty(2, 0.1)
        )
        end = TrackPosition(
            mstats.ValueUncertainty(2, 0.1),
            mstats.ValueUncertainty(3, 0.1)
        )

        l = geometry.LineSegment2D(start, end)
        length = l.length.raw

        post_delta = 1.2
        l.post_extend_line(post_delta, replace=False)

        self.assertAlmostEqual(l.start.x.raw, start.x.raw)
        self.assertAlmostEqual(l.start.y.raw, start.y.raw)
        self.assertAlmostEqual(l.end.x.raw, end.x.raw)
        self.assertAlmostEqual(l.end.y.raw, end.y.raw + post_delta)
        self.assertAlmostEqual(length + post_delta, l.length.raw)

        pre_delta = 2.3
        l.pre_extend_line(pre_delta, replace=False)

        self.assertAlmostEqual(l.start.x.raw, start.x.raw)
        self.assertAlmostEqual(l.start.y.raw, start.y.raw - pre_delta)
        self.assertAlmostEqual(l.end.x.raw, end.x.raw)
        self.assertAlmostEqual(l.end.y.raw, end.y.raw + post_delta)
        self.assertAlmostEqual(length + post_delta + pre_delta, l.length.raw)

    def test_line_extension_45(self):
        """
        """
        start = TrackPosition(
            mstats.ValueUncertainty(2, 0.1),
            mstats.ValueUncertainty(2, 0.1)
        )
        end = TrackPosition(
            mstats.ValueUncertainty(3, 0.1),
            mstats.ValueUncertainty(3, 0.1)
        )

        l = geometry.LineSegment2D(start, end)
        length = l.length.raw

        post_adjustment = 1.2
        post_delta = math.sqrt(2.0) * post_adjustment
        l.post_extend_line(post_delta, replace=False)

        self.assertAlmostEqual(l.start.x.raw, start.x.raw)
        self.assertAlmostEqual(l.start.y.raw, start.y.raw)
        self.assertAlmostEqual(l.end.x.raw, end.x.raw + post_adjustment)
        self.assertAlmostEqual(l.end.y.raw, end.y.raw + post_adjustment)
        self.assertAlmostEqual(length + post_delta, l.length.raw)

        pre_adjustment = 2.3
        pre_delta = math.sqrt(2) * pre_adjustment
        l.pre_extend_line(pre_delta, replace=False)

        self.assertAlmostEqual(l.start.x.raw, start.x.raw - pre_adjustment)
        self.assertAlmostEqual(l.start.y.raw, start.y.raw - pre_adjustment)
        self.assertAlmostEqual(l.end.x.raw, end.x.raw + post_adjustment)
        self.assertAlmostEqual(l.end.y.raw, end.y.raw + post_adjustment)
        self.assertAlmostEqual(length + post_delta + pre_delta, l.length.raw)


################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeometry)
    unittest.TextTestRunner(verbosity=2).run(suite)




