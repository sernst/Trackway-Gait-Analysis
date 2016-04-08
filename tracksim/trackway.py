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

    def __init__(
            self,
            x: mstats.value.ValueUncertainty,
            y: mstats.value.ValueUncertainty,
            **kwargs
    ):
        """ Initializes the TrackPosition with the arguments """

        assert isinstance(x, mstats.value.ValueUncertainty), \
            'x must be a ValueUncertainty instance'

        assert isinstance(y, mstats.value.ValueUncertainty), \
            'y must be a ValueUncertainty instance'

        self.__class__._instance_index += 1
        self.uid = self.__class__._instance_index

        self.x = x
        self.y = y
        self.annotation = kwargs.get('annotation')

    def rotate(
            self,
            angle: float,
            pivot: mstats.value.ValueUncertainty = None
    ):
        """
        Rotates the position value by the specified angle using a standard 2D
        rotation matrix formulation. If an origin Position2D instance is not
        specified the rotation will occur around the origin. Also, if an origin
        is specified, the uncertainty in that origin value will be propagated
        through to the uncertainty of the rotated result.

        :param angle:
            An angle (in radians) about which each track should be rotated
        :param pivot:
            The origin position about which the rotation will be applied. If
            no value is provided, the global origin (0, 0) will be used.
        """

        if pivot is None:
            pivot = TrackPosition(
                mstats.value.ValueUncertainty(),
                mstats.value.ValueUncertainty()
            )

        x = (self.x - pivot.x).raw
        y = (self.y - pivot.y).raw

        self.x.raw = x*math.cos(angle) - y*math.sin(angle) + pivot.x.raw
        self.y.raw = y*math.cos(angle) + x*math.sin(angle) + pivot.y.raw

        self.x.raw_uncertainty = math.sqrt(
                self.x.raw_uncertainty * self.x.raw_uncertainty +
                pivot.x.raw_uncertainty * pivot.x.raw_uncertainty
        )
        self.y.raw_uncertainty = math.sqrt(
                self.y.raw_uncertainty * self.y.raw_uncertainty +
                pivot.y.raw_uncertainty * pivot.y.raw_uncertainty
        )

    def clone(self) -> 'TrackPosition':
        """ Returns a copy of this TrackPosition """

        return TrackPosition(
            x=self.x.clone(),
            y=self.y.clone(),
            annotation=self.annotation
        )

    def echo(self) -> str:
        """ Returns a formatted string representation of this instance """

        return '[POS({}) x: {} +/- {} | y: {} +/- {}]'.format(
                self.uid,
                self.x.value, self.x.uncertainty,
                self.y.value, self.y.uncertainty)

    def __repr__(self):
        return self.echo()

    def __str__(self):
        return self.echo()

    def compare(self, comparison: 'TrackPosition') -> bool:
        """
        Compares the positions of this track position and the one specified by
        the comparison argument and returns True if their positions and
        uncertainties match.

        :param comparison:
            Another TrackPosition instance to compare with this instance
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

    def distance_between(
            self,
            position: 'TrackPosition'
    ) -> mstats.value.ValueUncertainty:
        """
        Returns the calculated distance between this position and the
        position argument

        :param position:
            Other TrackPosition to calculate the distance between
        """

        dx = position.x - self.x
        dy = position.y - self.y

        if mstats.value.equivalent(dx.value, 0.0):
            sum_for_error = dx + dy
            return mstats.value.ValueUncertainty(
                abs(dy.raw),
                sum_for_error.raw_uncertainty
            )

        if mstats.value.equivalent(dy.value, 0.0):
            sum_for_error = dx + dy
            return mstats.value.ValueUncertainty(
                abs(dx.raw),
                sum_for_error.raw_uncertainty
            )

        try:
            return (
                       dx ** 2 +
                       dy ** 2
                   ) ** 0.5
        except Exception as err:
            print('Positions:', self, position, err)
            raise

    @classmethod
    def from_raw_values(
            cls,
            x: float = 0.0,
            y: float = 0.0,
            x_uncertainty: float = 1.0,
            y_uncertainty: float = 1.0,
            **kwargs
    ) -> 'TrackPosition':
        """ Creates a trackway instance from raw numbers instead of directly
            from ValueUncertainties for the x and y values
        """

        return TrackPosition(
            x=mstats.value.ValueUncertainty(x, x_uncertainty),
            y=mstats.value.ValueUncertainty(y, y_uncertainty),
            **kwargs
        )


class TrackwayDefinition(object):
    """
    A data management class that contains the limb phases and positions for the
    simulation trial
    """

    def __init__(
            self,
            limb_positions: limb.Property = None,
            limb_phases: limb.Property = None
    ):
        """
        Assigns limb_positions and limb_phases to the trackway definition
        """

        self.limb_positions = limb_positions
        self.limb_phases = limb_phases

    def clone(self):
        """ Returns a deep copy of this instance """

        limb_phases = None
        if self.limb_phases:
            limb_phases = self.limb_positions.clone()

        limb_positions = None
        if self.limb_positions:
            limb_positions = self.limb_positions.clone()

        return TrackwayDefinition(limb_positions, limb_phases)

    def reorient_positions(self):
        """
        Reorient the trackway positions so that they begin at the origin and
        travel toward the +x axis. Returns this instance for method chaining
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
            y=mstats.value.ValueUncertainty(min_y, 0.001)
        )
        pivot = TrackPosition(
            x=mstats.value.ValueUncertainty(0, 0.0001),
            y=mstats.value.ValueUncertainty(0, 0.0001)
        )

        orientation_angle = sum(angles)/len(angles)

        for key in limb.KEYS:
            positions = self.limb_positions.get(key)
            for pos in positions:
                pos.x -= offset.x
                pos.y -= offset.y
                pos.rotate(angle=-orientation_angle, pivot=pivot)

        return self


def load_positions_file(path: str) -> limb.Property:
    """
    Loads a limb positions property object from the specified path to a CSV
    file with columns:

        lp_x, lp_dx, lp_y, lp_dy
        rp_x, rp_dx, rp_y, rp_dy
        lm_x, lm_dx, lm_y, lm_dy
        rm_x, rm_dx, rm_y, rm_dy

    :param path:
        The path to the positions file to be loaded
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
