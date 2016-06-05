from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math

import measurement_stats as mstats
from measurement_stats.angle import Angle

from tracksim.trackway import TrackPosition


class LineSegment2D(object):
    """A class for..."""

    def __init__(self, start: TrackPosition, end: TrackPosition):
        """Creates a new instance of LineSegment2D."""
        self.start = start.clone()
        self.end   = end.clone()

    @property
    def is_value(self):
        return bool(
            abs(self.end.x - self.start.x) + abs(self.end.y - self.start.y)
        )

    @property
    def length(self):
        """ The length of the line segment. """
        return self.start.distance_between(self.end)

    @property
    def angle(self):
        v = self.end.clone()
        v.x -= self.start.x
        v.y -= self.start.y

        vxUnc = (
            self.start.x.raw_uncertainty ** 2 +
            self.end.x.raw_uncertainty ** 2
        ) ** 0.5

        vyUnc = (
            self.start.y.raw_uncertainty ** 2 +
            self.end.y.raw_uncertainty ** 2
        ) ** 0.5

        value = math.atan2(v.y, v.x)
        lengthSqr = v.x.raw ** 2 + v.y.raw ** 2
        unc = abs(v.y / lengthSqr) * vxUnc + abs(v.x / lengthSqr) * vyUnc
        return Angle(radians=value, uncertainty=unc)

    @property
    def slope(self):
        """ Returns the slope of the line as a ValueUncertainty named tuple. """
        s       = self.start
        e       = self.end
        deltaX  = e.x - s.x
        deltaY  = e.y - s.y

        try:
            slope   = deltaY / deltaX
            unc = abs(1.0 / deltaX) * (
                s.y.raw_uncertainty + e.y.raw_uncertainty
            ) + abs(slope / deltaX) * (
                s.x.raw_uncertainty + e.x.raw_uncertainty
            )
            return mstats.ValueUncertainty(slope, unc)
        except Exception:
            return None

    @property
    def midpoint(self):
        """
        Returns the midpoint of the line as a PositionValue2D instance.
        """

        x = 0.5 * (self.start.x + self.end.x)
        y = 0.5 * (self.start.y + self.end.y)

        return TrackPosition(x=x, y=y)

    def serialize(self):
        """

        :return:
        """

        return dict(
            start=self.start.serialize(),
            end=self.end.serialize()
        )

    def from_dict(self, source):
        """

        :param source:
        :return:
        """

        self.start = mstats.ValueUncertainty()
        self.start.from_dict(source['start'])

        self.end = mstats.ValueUncertainty()
        self.end.from_dict(source['end'])

    def add_offset(self, point):
        """add_offset doc..."""

        self.start.x += point.x
        self.start.y += point.y
        self.end.x += point.x
        self.end.y += point.y

    def get_parametric_position(self, value, clamp=True):
        """get_parametric_position doc..."""

        if clamp:
            value = max(0.0, min(value, 1.0))

        x = self.start.x + value * (self.end.x - self.start.x)
        y = self.start.y + value * (self.end.y - self.start.y)

        return TrackPosition(x=x, y=y)

    def adjust_point_along_line(self, point, delta, inPlace=False):
        """adjust_point_along_line doc..."""

        if not inPlace:
            point = point.clone()

        remove = mstats.value2D.Point2D(
            x=self.start.x.clone(),
            y=self.start.y.clone()
        )
        remove.invert()
        remove = TrackPosition(x=remove.x, y=remove.y)

        line = self.clone()
        line.add_offset(remove)

        position = line.get_parametric_position(
            delta / self.length.raw,
            clamp=False
        )
        point.add(position)

        return point

    def rotate(self, angle: float, pivot=None):
        """rotate doc..."""

        self.start.rotate(angle, pivot=pivot)
        self.end.rotate(angle, pivot=pivot)

    def angle_between(self, line):
        """
        Returns an Angle instance that represents the angle between this line
        segment and the one specified in the arguments.
        """

        return self.angle.difference_between(line.angle)

    def angle_between_point(self, position):
        """angle_between_point doc..."""
        a = mstats.value2D.Point2D(
            x=self.end.x - self.start.x,
            y=self.end.y - self.start.y
        )

        b = mstats.value2D.Point2D(
            x=self.end.x - self.start.x,
            y=self.end.y - self.start.y
        )

        return b.angle_between(a)

    def clone(self):
        """
        Returns a new LineSegment2D that is a clone of this instance. The start
        and end points are cloned as well making a completely separate copy with
        no reference dependencies on this instance.
        """

        return LineSegment2D(
            start=self.start.clone(),
            end=self.end.clone()
        )

    def distance_to_point(self, point):
        """
        Calculates the smallest distance between the specified point and  this
        line segment using the standard formulation as described in:

            http://en.wikipedia.org \
                /wiki/Distance_from_a_point_to_a_line \
                #Line_defined_by_two_points
        """

        length = self.length.raw
        if not length:
            raise ValueError(
                'Cannot calculate point distance. Invalid line segment.'
            )

        sx = self.start.x.raw
        sx_unc = self.start.x.raw_uncertainty
        sy = self.start.y.raw
        sy_unc = self.start.y.raw_uncertainty

        ex = self.end.x.raw
        ex_unc = self.end.x.raw_uncertainty
        ey = self.end.y.raw
        ey_unc = self.end.y.raw_uncertainty

        px = point.x.raw
        px_unc = point.x.raw_uncertainty
        py = point.y.raw
        py_unc = point.y.raw_uncertainty

        deltaX = ex - sx
        deltaY = ey - sy

        if deltaX == 0.0:
            # Vertical Line
            distance = abs(sx - px)
        elif deltaY == 0.0:
            # Horizontal line
            distance = abs(sy - py)
        else:
            distance = abs(
                deltaY * px - deltaX * py - sx * ey + ex * sy
            ) / length

        B = deltaY * px - deltaX * py - sx * ey + ex * sy
        AbsB = abs(B)
        D = (deltaX * deltaX + deltaY * deltaY) ** 0.5
        DPrime = 1.0 / (deltaX * deltaX + deltaY * deltaY) ** (3.0 / 2.0)
        bBD = B / (AbsB * D)

        pointXErr = px_unc * abs(deltaY * B / (AbsB * D))
        pointYErr = py_unc * abs(deltaX * B / (AbsB * D))
        startXErr = sx_unc * abs(AbsB * DPrime + bBD * (py - ey))
        startYErr = sy_unc * abs(AbsB * DPrime + bBD * (ex - px))
        endXErr = ex_unc * abs(bBD * (sy - py) - AbsB * DPrime)
        endYErr = ey_unc * abs(bBD * (px - sx) - AbsB * DPrime)
        error = (
            pointXErr + pointYErr +
            startXErr + startYErr +
            endXErr + endYErr
        )

        return mstats.ValueUncertainty(distance, error)

    def closest_point_on_line(self, point, contained=True):
        """
        Finds the closest point on a line to the specified point using the
        formulae discussed in the "another formula" section of:
            http://en.m.wikipedia.org \
                /wiki/Distance_from_a_point_to_a_line \
                #Another_formula
        """

        length = self.length.raw
        if not length:
            raise ValueError('Cannot calculate point. Invalid line segment.')

        sx = self.start.x.raw
        sx_unc = self.start.x.raw_uncertainty
        sy = self.start.y.raw
        sy_unc = self.start.y.raw_uncertainty

        ex = self.end.x.raw
        ex_unc = self.end.x.raw_uncertainty
        ey = self.end.y.raw
        ey_unc = self.end.y.raw_uncertainty

        px = point.x.raw
        px_unc = point.x.raw_uncertainty
        py = point.y.raw
        py_unc = point.y.raw_uncertainty

        deltaX = ex - sx
        deltaY = ey - sy
        rotate = False
        slope = 0.0
        slopeUnc = 0.0

        try:
            slope = deltaY / deltaX
            slopeUnc = (
                abs(1.0 / deltaX) * (sy_unc + ey_unc) +
                abs(slope / deltaX) * (sx_unc + ex_unc)
            )
        except Exception:
            rotate = True

        if rotate or (abs(slope) > 1.0 and abs(slopeUnc / slope) > 0.5):
            a = Angle(degrees=20.0)
            line = self.clone()
            line.rotate(a.value, self.start)
            p = point.clone()
            p.rotate(a, self.start)
            result = line.closest_point_on_line(p, contained=contained)
            if result is None:
                return result

            a.degrees = -20.0
            result.rotate(a.radians, self.start)
            return result

        intercept = sy - slope * sx
        denominator = slope * slope + 1.0
        numerator = point.x + slope * (point.y - intercept)

        x = (numerator / denominator).raw
        y = ((slope * numerator) / denominator + intercept).raw

        if contained:
            # Check to see if point is between start and end values
            xRange = sorted([sx, ex])
            yRange = sorted([sy, ey])
            eps = 1e-8
            xMin = x - eps
            xMax = x + eps
            yMin = y - eps
            yMax = y + eps
            outside = (
                xRange[1] < xMin or
                xMax < xRange[0] or
                yRange[1] < yMin or
                yMax < yRange[0]
            )
            if outside:
                return None

        startDist = self.start.distance_from(x, y)
        endDist = self.end.distance_from(x, y)

        x_unc = (
            startDist / length * sx_unc +
            endDist / length * ex_unc
        )
        x_unc = (x_unc ** 2 + px_unc ** 2) ** 0.5

        y_unc = (
            startDist / length * sy_unc +
            endDist / length * ey_unc
        )
        y_unc = (y_unc ** 2 + py_unc ** 2) ** 0.5

        return TrackPosition(
            x=mstats.ValueUncertainty(x, x_unc),
            y=mstats.ValueUncertainty(y, y_unc)
        )

    def post_extend_line(self, lengthAdjust, replace=True):
        """extendLine doc..."""
        newX, newY = self._extrapolate_by_length(lengthAdjust, pre=False)
        if not replace:
            self.end = self.end.clone()
        self.end.x = newX
        self.end.y = newY

    def pre_extend_line(self, lengthAdjust, replace=True):
        """pre_extend_line doc..."""
        newX, newY = self._extrapolate_by_length(lengthAdjust, pre=True)
        if not replace:
            self.start = self.start.clone()
        self.start.x = newX
        self.start.y = newY

    def create_next_line_segment(self, length=None):
        """
        Creates a line segment using this line segment as a guide that starts
        where this segment ends and has the same slope and orientation. The new
        line segment will be of the specified length, or if no length is
        specified the same length as this line segment.
        """

        if length is None:
            length = self.length

        target = self.clone()
        target.post_extend_line(lengthAdjust=length)
        target.start = self.end.clone()

        return target

    def create_previous_line_segment(self, length=None):
        """
        Creates a line segment using this line segment as a guide that ends
        where this segment begins and has the same slope and orientation. The
        new line segment will be of the specified length, or if no length is
        specified the same length as this line segment.
        """

        if length is None:
            length = self.length

        target = self.clone()
        target.pre_extend_line(lengthAdjust=length)
        target.end = self.start.clone()

        return target

    def _extrapolate_by_length(self, lengthAdjust, pre=False):
        """
        _extrapolate_by_length doc...
        """

        sx = self.start.x
        sy = self.start.y

        ex = self.end.x
        ey = self.end.y

        if pre:
            startY = sy
            startX = sx
            point = self.end
        else:
            startY = ey
            startX = ex
            point = self.start

        deltaX = startX - point.x
        deltaY = startY - point.y

        try:
            if mstats.value.equivalent(deltaX.value, 0.0):
                direction = deltaY.raw / abs(deltaY.raw)
                return startX, startY + direction * lengthAdjust

            if mstats.value.equivalent(deltaY.value, 0.0):
                direction = deltaX.raw / abs(deltaX.raw)
                return startX + direction * lengthAdjust, startY
        except ZeroDivisionError as err:
            print('Zero Division Error:')
            print('Delta X: {} Delta Y: {}'.format(deltaX, deltaY))
            print('Line Start: ({}, {})'.format(self.start.x, self.start.y))
            print('Line End: ({}, {})'.format(self.end.x, self.end.y))
            raise

        deltaX = startX - point.x
        deltaY = startY - point.y

        angle = math.atan2(deltaY.raw, deltaX.raw)

        return (
            startX + lengthAdjust * math.cos(angle),
            startY + lengthAdjust * math.sin(angle)
        )
