
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

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

        x = self.x - origin.x
        y = self.y - origin.y

        self.x.raw = x*math.cos(angle) - y*math.sin(angle) + origin.x
        self.y.raw = y*math.cos(angle) + x*math.sin(angle) + origin.y

        self.x.raw_uncertainty = math.sqrt(
                self.x.uncertainty * self.x.uncertainty +
                origin.x.uncertainty * origin.x.uncertainty)
        self.y.raw_uncertainty = math.sqrt(
                self.y.uncertainty * self.y.uncertainty +
                origin.y.uncertainty * origin.y.uncertainty)

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

            angle = math.atan2(y, x)

            orientation_angle = angle if \
                abs(angle) > abs(orientation_angle) else \
                orientation_angle

        offset = TrackPosition(min_x, min_y)
        origin = TrackPosition(0, 0)

        for key in tracksim.LimbProperty.LIMB_KEYS:
            positions = self.limb_positions.get(key)
            for pos in positions:
                pos.x -= offset.x
                pos.y -= offset.y
                pos.rotate(angle=orientation_angle, origin=origin)



