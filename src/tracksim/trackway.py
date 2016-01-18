
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pandas as pd
import numpy as np
import math

import tracksim
from tracksim import number

class TrackPosition(object):
    """
        Class representation a track print position in 2D space (x, y) with
        uncertainty values x_unc and y_unc in the form:

        (x +/- x_unc, y +/- y_unc)

    """

    _instance_index = 0

    def __init__(self, x, y, **kwargs):
        assert isinstance(x, number.ValueUncertainty), \
            'x must be a ValueUncertainty instance'

        assert isinstance(y, number.ValueUncertainty), \
            'y must be a ValueUncertainty instance'

        self._instance_index += 1
        self.uid = self._instance_index

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

    @classmethod
    def from_raw_values(cls, x, y, x_uncertainty, y_uncertainty, **kwargs):
        return TrackPosition(
            x=number.ValueUncertainty(x, x_uncertainty),
            y=number.ValueUncertainty(y, y_uncertainty),
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

        orientation_angle = 0
        for key in tracksim.LimbProperty.LIMB_KEYS:
            positions = self.limb_positions.get(key)
            for pos in positions:
                min_x = min(pos.x.value, min_x)
                min_y = min(pos.y.value, min_y)

            x = positions[-1].x - positions[0].x
            y = positions[-1].y - positions[0].y

            angle = math.atan2(y.value, x.value)

            orientation_angle = angle if \
                abs(angle) > abs(orientation_angle) else \
                orientation_angle

        offset = TrackPosition(
                x=number.ValueUncertainty(min_x, 0.001),
                y=number.ValueUncertainty(min_y, 0.001) )
        origin = TrackPosition(
                x=number.ValueUncertainty(0, 0.0001),
                y=number.ValueUncertainty(0, 0.0001) )

        for key in tracksim.LimbProperty.LIMB_KEYS:
            positions = self.limb_positions.get(key)
            for pos in positions:
                pos.x -= offset.x
                pos.y -= offset.y
                pos.rotate(angle=orientation_angle, origin=origin)



def load_positions_file(path):
    """

    :param path:
    :return:
    """
    df = pd.read_csv(path)

    trackway_positions = tracksim.LimbProperty().assign([], [], [], [])

    for index, series in df.iterrows():
        if series.lpxunc and not np.isnan(series.lpxunc):
            trackway_positions.left_pes.append(
                TrackPosition.from_raw_values(
                    x=series.lpx, x_uncertainty=series.lpxunc,
                    y=series.lpy, y_uncertainty=series.lpyunc ))

        if series.rpxunc and not np.isnan(series.rpxunc):
            trackway_positions.right_pes.append(
                TrackPosition.from_raw_values(
                    x=series.rpx, x_uncertainty=series.rpxunc,
                    y=series.rpy, y_uncertainty=series.rpyunc ))

        if series.lmxunc and not np.isnan(series.lmxunc):
            trackway_positions.left_manus.append(
                TrackPosition.from_raw_values(
                    x=series.lmx, x_uncertainty=series.lmxunc,
                    y=series.lmy, y_uncertainty=series.lmyunc ))

        if series.rmxunc and not np.isnan(series.rmxunc):
            trackway_positions.right_manus.append(
                TrackPosition.from_raw_values(
                    x=series.rmx, x_uncertainty=series.rmxunc,
                    y=series.rmy, y_uncertainty=series.rmyunc ))

    if not trackway_positions.left_manus:
        for pos in trackway_positions.left_pes:
            trackway_positions.left_manus.append(pos.clone())

    if not trackway_positions.right_manus:
        for pos in trackway_positions.right_pes:
            trackway_positions.right_manus.append(pos.clone())

    return trackway_positions
