import random
import unittest

from tracksim import generate
from tracksim import limb


class test_generate(unittest.TestCase):

    def test_track_positions(self):
        """
            Confirms positions generated are
        """

        count = 10
        step_size = 4.2
        lateral_displacement = 0.4

        positions = generate.track_positions(
                cycle_count=count,
                step_size=step_size,
                track_offset=0,
                lateral_displacement=lateral_displacement)

        self.assertEqual(len(positions), count)
        for i in range(len(positions)):
            self.assertAlmostEqual(positions[i].x.value, i*step_size)

    def test_trackway_positions(self):
        """

        :return:
        """

        count = 12
        step_size = 3.7
        lateral_displacement = 0.2

        phases = limb.Property(
            left_pes=0.0,
            right_pes=0.5,
            left_manus=0.25,
            right_manus=0.75
        )

        positions = generate.trackway_positions(
            cycle_count=count,
            step_size=step_size,
            track_offsets=phases,
            lateral_displacement=lateral_displacement
        )

        self.assertIsInstance(positions, limb.Property)

        for key, series in positions.items():
            self.assertEqual(len(series), count)
            self.assertAlmostEquals(
                    step_size,
                    series[1].x.value - series[0].x.value)

    def test_time_steps(self):
        """
            Tests time step generation
        """

        for i in range(10):
            min_value = random.uniform(-1000.0, 1000.0)
            max_value = random.uniform(min_value + 1.0, min_value + 1000.0)
            steps_per_cycle = random.randint(10, 1000)
            out = generate.time_steps(steps_per_cycle, min_value, max_value)

            try:
                self.assertAlmostEquals(out[-1], max_value)
                self.assertAlmostEquals(out[0], min_value)
            except AssertionError as err:
                print('INPUT:', {
                    'min':min_value,
                    'max':max_value,
                    'steps':steps_per_cycle})
                print('OUTPUT:', {
                    'min':out[0],
                    'max':out[-1],
                    'length':len(out)})
                raise

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_generate)
    unittest.TextTestRunner(verbosity=2).run(suite)



