from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

LEFT_PES = 'left_pes'
RIGHT_PES = 'right_pes'
LEFT_MANUS = 'left_manus'
RIGHT_MANUS = 'right_manus'

# The keys for each of the limbs
KEYS = [LEFT_PES, RIGHT_PES, LEFT_MANUS, RIGHT_MANUS]
SHORT_KEYS = ['lp', 'rp', 'lm', 'rm']

# Map between short-format and long-format keys for each limb
LIMB_KEY_LOOKUP = {
    SHORT_KEYS[0]: KEYS[0],
    SHORT_KEYS[1]: KEYS[1],
    SHORT_KEYS[2]: KEYS[2],
    SHORT_KEYS[3]: KEYS[3]
}

class Property(object):
    """ A class that describes an attribute with potentially unique values for
        each limb within the quadrupedal system.
    """

    def __init__(self, **kwargs):
        self.left_pes = kwargs.get(LEFT_PES)
        self.right_pes = kwargs.get(RIGHT_PES)
        self.left_manus = kwargs.get(LEFT_MANUS)
        self.right_manus = kwargs.get(RIGHT_MANUS)

    def get(self, key, default = None):
        """ Retrieve the value for the limb specified by the key

        :param key: The limb key for which to retrieve the value.
        :param default: The value returned if the value stored in the limb
            property is None.
        :return: The value, or its default, for the specified limb.
        """

        if not hasattr(self, key):
            if key in LIMB_KEY_LOOKUP:
                key = LIMB_KEY_LOOKUP[key]
            else:
                raise KeyError('"{}" not a valid Property key'.format(key))

        out = getattr(self, key)
        return default if out is None else out

    def set(self, key, value):
        """ Sets the value for the specified key

        :param key: Either a long or short key name for the limb on which to
            set the property.
        :param value: The value to set for the specified limb
        :return: self
        :rtype: Property
        """

        if not hasattr(self, key):
            if key in LIMB_KEY_LOOKUP:
                key = LIMB_KEY_LOOKUP[key]
            else:
                raise KeyError('"{}" not a valid Property key'.format(key))
        setattr(self, key, value)

        return self

    def assign(self, *args, **kwargs):
        """ Sets the values for each of the limb properties in the arguments
            list with a non-None value.

        :return: self
        :rtype: Property
        """

        for i in range(len(args)):
            value = args[i]
            if value is not None:
                self.set(KEYS[i], value)

        for short_key, long_key in LIMB_KEY_LOOKUP.items():
            if short_key in kwargs and kwargs[short_key] is not None:
                self.set(long_key, kwargs[short_key])
            elif long_key in kwargs and kwargs[long_key] is not None:
                self.set(long_key, kwargs[long_key])

        return self

    def items(self):
        """ Key-value pairs for each limb

        :return: A tuple where each element is a 2-tuple containing a key
            and value pair for each limb.
        :rtype: tuple
        """

        return (
            (LEFT_PES, self.left_pes),
            (RIGHT_PES, self.right_pes),
            (LEFT_MANUS, self.left_manus),
            (RIGHT_MANUS, self.right_manus)
        )

    def values(self):
        """ Values for each limb

        :return: A tuple containing the limb-ordered values of
        :rtype: list
        """

        return (
            self.left_pes,
            self.right_pes,
            self.left_manus,
            self.right_manus
        )

    def toDict(self):
        """ Converts the Property instance to a dictionary

        :return: A dictionary with the keys and values of the Property
        :rtype: dict
        """

        return {
            LEFT_PES:self.left_pes,
            RIGHT_PES:self.right_pes,
            LEFT_MANUS:self.left_manus,
            RIGHT_MANUS:self.right_manus
        }
