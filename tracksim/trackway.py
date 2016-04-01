from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math

import numpy as np
import pandas as pd

import measurement_stats as mstats
from tracksim import limb


class TrackPosition(object):
    """
        Class representation a track print position in 2D space (x, y) with
        uncertainty values x_unc and y_unc in the form:

        (x +/- x_unc, y +/- y_unc)

    """

    _instance_index = 0

    def __init__(self, x, y, **kwargs):
        assert isinstance(x, mstats.value.ValueUncertainty), \
            'x must be a ValueUncertainty instance'

        assert isinstance(y, mstats.value.ValueUncertainty), \
            'y must be a ValueUncertainty instance'

        self.__class__._instance_index += 1
        self.uid = self.__class__._instance_index

        self.x = x
        self.y = y
        self.annotation = kwargs.get('annotation')

    def rotate(self, angle, origin =None):
        """ Rotates the position value by the specified angle using a standard
            2D rotation matrix formulation. If an origin Position2D instance is
            not specified the rotation will occur around the origin. Also, if
            an origin is specified, the uncertainty in that origin value will
            be propagated through to the uncertainty of the rotated result.

        :param angle:
        :param origin:
        :returns:
        """

        if origin is None:
            origin = TrackPosition(0, 0)

        x = (self.x - origin.x).raw
        y = (self.y - origin.y).raw

        self.x.raw = x*math.cos(angle) - y*math.sin(angle) + origin.x.raw
        self.y.raw = y*math.cos(angle) + x*math.sin(angle) + origin.y.raw

        self.x.raw_uncertainty = math.sqrt(
                self.x.raw_uncertainty * self.x.raw_uncertainty +
                origin.x.raw_uncertainty * origin.x.raw_uncertainty)
        self.y.raw_uncertainty = math.sqrt(
                self.y.raw_uncertainty * self.y.raw_uncertainty +
                origin.y.raw_uncertainty * origin.y.raw_uncertainty)

    def clone(self):
        return TrackPosition(
            x=self.x.clone(),
            y=self.y.clone(),
            annotation=self.annotation)

    def echo(self):
        return '[POS({}) x: {} +/- {} | y: {} +/- {}]'.format(
                self.uid,
                self.x.value, self.x.uncertainty,
                self.y.value, self.y.uncertainty)

    def __repr__(self):
        return self.echo()

    def __str__(self):
        return self.echo()

    def compare(self, comparison):
        """ Compares the positions of this track position and the one specified
            by the comparison argument and returns True if their positions and
            uncertainties match.
        :param comparison:
        """

        equal = mstats.value.equivalent
        if not equal(self.x.value, comparison.x.value):
            return False
        elif not equal(self.y.value, comparison.y.value):
            return False
        elif not equal(self.x.uncertainty, comparison.x.uncertainty):
            return False
        elif not equal(self.y.uncertainty, comparison.y.uncertainty):
            return False

        return True

    @classmethod
    def from_raw_values(cls, x, y, x_uncertainty, y_uncertainty, **kwargs):
        return TrackPosition(
            x=mstats.value.ValueUncertainty(x, x_uncertainty),
            y=mstats.value.ValueUncertainty(y, y_uncertainty),
            **kwargs)

class TrackwayDefinition(object):
    """

    """

    def __init__(self, **kwargs):
        self.limb_positions = kwargs.get('limb_positions')
        self.limb_phases = kwargs.get('limb_phases')

    def reorient_positions(self):
        """
            Reorient the trackway positions so that they begin at the origin
            and travel toward the +x axis.

        :return:
        """

        min_x = 1e12
        min_y = 1e12
        angles = []

        for key in limb.KEYS:
            positions = self.limb_positions.get(key)

            for pos in positions:
                min_x = min(pos.x.value, min_x)
                min_y = min(pos.y.value, min_y)

            x = positions[-1].x - positions[0].x
            y = positions[-1].y - positions[0].y

            angles.append(math.atan2(y.value, x.value))

        offset = TrackPosition(
                x=mstats.value.ValueUncertainty(min_x, 0.001),
                y=mstats.value.ValueUncertainty(min_y, 0.001) )
        origin = TrackPosition(
                x=mstats.value.ValueUncertainty(0, 0.0001),
                y=mstats.value.ValueUncertainty(0, 0.0001) )

        orientation_angle = sum(angles)/len(angles)

        for key in limb.KEYS:
            positions = self.limb_positions.get(key)
            for pos in positions:
                pos.x -= offset.x
                pos.y -= offset.y
                pos.rotate(angle=-orientation_angle, origin=origin)

def load_positions_file(path):
    """

    :param path:
    :return:
    """
    df = pd.read_csv(path)

    trackway_positions = limb.Property().assign([], [], [], [])

    def add_track(limb_data, x, dx, y, dy):
        if not dx or np.isnan(dx) or not dy or np.isnan(dy):
            # Don't add track if the uncertainty values are invalid, which is
            # an indicator that the row is not a valid position
            return

        limb_data.append(TrackPosition.from_raw_values(
            x=x, x_uncertainty=dx, y=y, y_uncertainty=dy
        ))

    for index, series in df.iterrows():

        for prefix, limb_key in limb.LIMB_KEY_LOOKUP.items():
            try:
                add_track(
                    limb_data=trackway_positions.get(limb_key),
                    x=series['{}_x'.format(prefix)],
                    dx=series['{}_dx'.format(prefix)],
                    y=series['{}_y'.format(prefix)],
                    dy=series['{}_dy'.format(prefix)]
                )
            except KeyError:
                # If the key is missing in the csv file, move one
                continue

    if not trackway_positions.left_manus:
        for pos in trackway_positions.left_pes:
            trackway_positions.left_manus.append(pos.clone())

    if not trackway_positions.right_manus:
        for pos in trackway_positions.right_pes:
            trackway_positions.right_manus.append(pos.clone())

    return trackway_positions
