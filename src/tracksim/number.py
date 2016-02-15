from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import sys
import random

if sys.version > '3':
    long = int

try:
    import numpy as np
except Exception:
    np = None

def divide_value_uncertainties(numeratorValue, denominatorValue):
    """
        Divides two ValueUncertainty instances to produce a new one with error
        propagation.

    :param numeratorValue:
    :param denominatorValue:
    :return:
    """

    n = numeratorValue
    d = denominatorValue
    val = n.raw/d.raw
    unc = val*math.sqrt(
            (n.rawUncertainty/n.raw)**2 +
            (d.rawUncertainty/d.raw)**2 )
    return ValueUncertainty(val, unc)

def average(*values):
    """

    :param values:
    :return:
    """

    if not values:
        return ValueUncertainty()

    if isinstance(values[0], (list, tuple)):
        values = values[0]
        if not values:
            return ValueUncertainty()

    vals = []
    for v in values:
        vals.append(v.value)

    return ValueUncertainty(
            value=float(np.mean(vals)),
            uncertainty=float(np.std(vals)) )

def weighted_average(*values):
    """
        Calculates the uncertainty weighted average of the provided values,
        where each value is a ValueUncertainty instance. For mathematical
        formulation of the weighted average see "An Introduction to Error
        Analysis, 2nd Edition" by John R. Taylor, Chapter 7.2.

    :param values:
    :return:
    """

    if not values:
        return ValueUncertainty()

    if isinstance(values[0], (list, tuple)):
        values = values[0]
        if not values:
            return ValueUncertainty()

    wxs = 0.0
    ws  = 0.0
    for v in values:
        w = 1.0/(v.uncertainty*v.uncertainty)
        wxs += w*v.value
        ws  += w

    ave = wxs/ws
    unc =  1.0/math.sqrt(ws)

    return ValueUncertainty(value=ave, uncertainty=unc)

def order_of_magnitude(value):
    """
        Returns the order of magnitude of the most significant digit of the
        specified number. A value of zero signifies the ones digit, as would be
        the case in [Number]*10^[Order].

    :param value:
    :return:
    """

    x = abs(float(value))
    offset = 0 if x >= 1.0 else -1
    return int(math.log10(x) + offset)

def sqrt_sum_of_squares(*args):
    """

    :param args:
    :return:
    """

    out = 0.0
    for arg in args:
        out += float(arg) * float(arg)

    return math.sqrt(out)

def equivalent(a, b, epsilon = None, machineEpsilonFactor = 100.0):
    """

    :param a:
    :param b:
    :param epsilon:
    :param machineEpsilonFactor:
    :return:
    """

    if epsilon is None:
        epsilon = machineEpsilonFactor * sys.float_info.epsilon
    return abs(float(a) - float(b)) < epsilon

def round_to_order(value, order, round_op = None, asInt = False):
    """

    :param value:
    :param order:
    :param round_op:
    :param asInt:
    :return:
    """

    if round_op is None:
        round_op = round

    if order == 0:
        value = round(float(value))
        return int(value) if asInt else value

    scale = math.pow(10, order)
    value = scale * round_op(float(value) / scale)
    return int(value) if asInt else value

def round_significant(value, digits):
    """

    :param value:
    :param digits:
    :return:
    """

    if value == 0.0:
        return 0

    value = float(value)
    d = math.ceil(math.log10(-value if value < 0  else value))
    power = digits - int(d)

    magnitude = math.pow(10, power)
    shifted = round(value*magnitude)
    return shifted / magnitude

def least_significant_order(value):
    """

    :param value:
    :return:
    """

    om = 0

    if isinstance(value, (int, long)) or long(value) == value:
        value = long(value)

        while om < 10000:
            om += 1
            magnitude = math.pow(10, -om)
            test = float(value) * magnitude
            if long(test) != test:
                return om - 1
        return 0

    while om < 10000:
        om -= 1
        magnitude = math.pow(10, -om)
        test = value * magnitude
        if equivalent(test, int(test)):
            return om
    return 0

def mean_and_deviation(*values):
    """

    :param values:
    :return:
    """

    if np is None:
        raise ImportError('mean_and_deviation() requires Numpy')

    if not values:
        return ValueUncertainty()

    if isinstance(values[0], (list, tuple)):
        values = values[0]
        if not values:
            return ValueUncertainty()

    vals = []
    for value in values:
        try:
            vals.append(value.value)
        except Exception:
            vals.append(value)

    try:
        mean    = np.mean(vals, dtype=np.float64)
        std     = np.std(vals, dtype=np.float64)
        return ValueUncertainty(float(mean), float(std))
    except Exception as err:
        raise

def weighted_mean_and_deviation(*values):
    """
        Returns the mean and standard deviation of a weighted set of values.
        For further info see:
            http://stats.stackexchange.com/questions/6534/
                how-do-i-calculate-a-weighted-standard-deviation-in-excel

    :param values:
    :return:
    """

    if np is None:
        raise ImportError('NumericUtils.getMeanAndDeviation() requires Numpy')

    if not values:
        return ValueUncertainty()

    if isinstance(values[0], (list, tuple)):
        values = values[0]
        if not values:
            return ValueUncertainty()

    if len(values) == 1:
        return values[0].clone()

    wxs = 0.0
    ws  = 0.0
    weights = []

    for v in values:
        w = 1.0/(v.uncertainty*v.uncertainty)
        weights.append(w)
        wxs += w*v.value
        ws  += w

    ave = wxs/ws
    dev = 0.0
    N = len(values)
    for i in range(N):
        dev += weights[i]*(values[i].value - ave)**2

    denom = ws*(N - 1.0)/N
    dev = math.sqrt(dev/denom)

    return ValueUncertainty(value=ave, uncertainty=dev)

def is_number(value):
    """

    :param value:
    :return:
    """
    return isinstance(value, (int, long, float))

def linear_space(min_value = 0, max_value = 1.0, length = 10, round_op = None):
    """
        Returns a list of linear-spaced values with min_value and max_value as
        the boundaries with the specified number (length) of entries. If
        roundToIntegers is True, each value will be rounded to the nearest
        integer.

    :param min_value:
    :param max_value:
    :param length:
    :param round_op:
    :return:
    """

    out     = []
    value   = min_value
    length  = max(2, length)
    delta   = (float(max_value) - float(min_value)) / float(length - 1.0)

    for index in range(length - 1):
        out.append(round_op(value) if round_op else value)
        value += delta

    out.append(round_op(max_value) if round_op else max_value)
    return out

def deviations(expected, values):
    """

    :param expected:
    :param values:
    :return:
    """

    out = []

    if hasattr(expected, 'raw_uncertainty'):
        for v in values:
            err = math.sqrt(
                v.raw_uncertainty ** 2 +
                expected.raw_uncertainty ** 2
            )
            out.append(abs(v.raw - expected.raw) / err)
    else:
        for v in values:
            out.append(abs(v.value - expected) / v.uncertainty)

    return out

class ValueUncertainty(object):
    """

    """

    def __init__(self, value =0.0, uncertainty =1.0, **kwargs):
        self.raw = float(value)
        self.raw_uncertainty = abs(float(uncertainty))

    @property
    def value(self):
        uncertainty = self.uncertainty
        order       = least_significant_order(uncertainty)
        return round_to_order(self.raw, order)

    @property
    def uncertainty(self):
        return round_significant(abs(self.raw_uncertainty), 1)

    @property
    def html_label(self):
        return '%.15g &#177; %s' % (self.value, self.uncertainty)

    @property
    def label(self):
        return '%.15g +/- %s' % (self.value, self.uncertainty)

    @property
    def raw_label(self):
        return '%.15g +/- %.15g' % (
            round_significant(self.raw, 6),
            self.uncertainty)

    def from_dict(self, source):
        self.raw = source['raw']
        self.raw_uncertainty = source['raw_uncertainty']

    def to_dict(self):
        return {
            'value': self.value,
            'uncertainty': self.uncertainty,
            'raw': self.raw,
            'raw_uncertainty': self.raw_uncertainty }

    def clone(self):
        """clone doc..."""
        return ValueUncertainty(
            value=self.raw,
            uncertainty=self.raw_uncertainty)

    def update(self, value = None, uncertainty = None):

        if value is not None:
            self.raw = value

        if uncertainty is not None:
            self.raw_uncertainty = uncertainty

    @classmethod
    def createRandom(
            cls, min_value =-1.0, max_value =1.0,
            min_uncertainty =0.1, max_uncertainty =2.0
    ):
        """

        :param min_value:
        :param max_value:
        :param min_uncertainty:
        :param max_uncertainty:
        :return:
        """

        return ValueUncertainty(
            value=random.uniform(min_value, max_value),
            uncertainty=random.uniform(min_uncertainty, max_uncertainty) )

    def __pow__(self, power, modulo=None):
        if equivalent(self.raw, 0.0):
            return ValueUncertainty(self.raw, self.raw_uncertainty)

        val = self.raw ** power
        unc = abs(val * float(power) * self.raw_uncertainty / self.raw)
        return ValueUncertainty(val, unc)

    def __add__(self, other):
        try:
            val = self.raw + other.raw
            unc = math.sqrt(
                    self.raw_uncertainty ** 2 +
                    other.raw_uncertainty ** 2 )
        except Exception:
            val = float(other) + self.raw
            unc = self.raw_uncertainty

        return ValueUncertainty(val, unc)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        try:
            val = self.raw - other.raw
            unc = math.sqrt(
                    self.raw_uncertainty ** 2 +
                    other.raw_uncertainty ** 2 )
        except Exception:
            val = self.raw - float(other)
            unc = self.raw_uncertainty

        return ValueUncertainty(val, unc)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        try:
            val = self.raw*other.raw
            unc = abs(val)*math.sqrt(
                (self.raw_uncertainty / self.raw) ** 2 +
                (other.raw_uncertainty / other.raw) ** 2)
        except Exception:
            val = float(other) * self.raw
            unc = abs(float(other) * self.raw_uncertainty)

        return ValueUncertainty(val, unc)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        try:
            val = self.raw/other.raw
            unc = abs(val) * math.sqrt(
                (self.raw_uncertainty / self.raw) ** 2 +
                (other.raw_uncertainty / other.raw) ** 2)
        except Exception:
            val = self.raw / float(other)
            unc = abs(self.raw_uncertainty / float(other))

        return ValueUncertainty(val, unc)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __div__(self, other):
        return self.__truediv__(other)

    def __rdiv__(self, other):
        return self.__rtruediv__(other)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        """__unicode__ doc..."""
        return '<%s %s>' % (self.__class__.__name__, self.label)

    def __str__(self):
        return '<%s %s>' % (self.__class__.__name__, self.label)

