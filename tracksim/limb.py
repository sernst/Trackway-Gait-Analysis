import json
import typing

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
    """
    A class that describes an attribute with potentially unique values for each
    limb within the quadrupedal system.
    """

    def __init__(self, **kwargs):
        self.left_pes = kwargs.get(LEFT_PES)
        self.right_pes = kwargs.get(RIGHT_PES)
        self.left_manus = kwargs.get(LEFT_MANUS)
        self.right_manus = kwargs.get(RIGHT_MANUS)

    def get(self, key: str, default=None):
        """
        Retrieve the value for the limb specified by the key

        :param key:
            The limb key for which to retrieve the value
        :param default:
            The value returned if the value stored in the limb property is None
        """

        if not hasattr(self, key):
            if key in LIMB_KEY_LOOKUP:
                key = LIMB_KEY_LOOKUP[key]
            else:
                raise KeyError('"{}" not a valid Property key'.format(key))

        out = getattr(self, key)
        return default if out is None else out

    def set(self, key: str, value) -> 'Property':
        """
        Sets the value for the specified key and returns this instance for
        method chaining

        :param key:
            Either a long or short key name for the limb on which to set the
            property
        :param value:
            The value to set for the specified limb
        """

        if not hasattr(self, key):
            if key in LIMB_KEY_LOOKUP:
                key = LIMB_KEY_LOOKUP[key]
            else:
                raise KeyError('"{}" not a valid Property key'.format(key))
        setattr(self, key, value)

        return self

    def assign(self, *args, **kwargs) -> 'Property':
        """
        Sets the values for each of the limb properties in the arguments list
        with a non-None value. Returns this instance for method chaining
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

    def items(self) -> typing.Tuple[tuple]:
        """
        Key-value pairs for each limb as a tuple where each element is a
        2-tuple containing a key and value pair for each limb.
        """

        return (
            (LEFT_PES, self.left_pes),
            (RIGHT_PES, self.right_pes),
            (LEFT_MANUS, self.left_manus),
            (RIGHT_MANUS, self.right_manus)
        )

    def values(self) -> tuple:
        """
        Values for each limb as a tuple containing the limb-ordered values of
        the Property
        """

        return (
            self.left_pes,
            self.right_pes,
            self.left_manus,
            self.right_manus
        )

    def to_dict(self) -> dict:
        """
        Converts the Property instance to a dictionary with the keys and values
        of the Property
        """

        return {
            LEFT_PES: self.left_pes,
            RIGHT_PES: self.right_pes,
            LEFT_MANUS: self.left_manus,
            RIGHT_MANUS: self.right_manus
        }

    def clone(self):
        """
        Returns a deep copy of the Property instance. The clone attempts to
        create a deep copy of each limb value by the following methods:

        1. If the value has a clone method, attempts to call that clone method.
        2. Serializing and then de-serializing the value if it is an
            appropriate type for that conversion
        3. Assume that the value is primitive and immutable and can be used
            directly in a copy
        """

        def deep_copy(value):
            try:
                if hasattr(value, 'clone'):
                    value.clone()
            except Exception:
                pass

            try:
                json.loads(json.dumps(value))
            except Exception:
                pass

            return value

        out = Property()
        for k in KEYS:
            out.set(k, deep_copy(self.get(k)))
        return out
