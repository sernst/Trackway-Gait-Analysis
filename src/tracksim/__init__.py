
import os

MY_PATH = os.path.abspath(os.path.dirname(__file__))

def make_project_path(*args):
    """
    Creates an absolute path to a file or folder within the trackway gait
    analysis project using the relative path elements specified by the
    args.

    :param args:
        Zero or more relative path elements that describe a file or folder
        within the project

    :return:
        An absolute path to the given file or folder
    """

    return os.path.abspath(os.path.join(MY_PATH, '..', '..', *args))

def make_resource_path(*args):
    """
    Creates an absolute path to a file or folder within the resources
    folder of the trackway gait analysis project using the relative path
    elements specified by the args.

    :param args:
        Zero or more relative path elements that describe a file or folder
        within the resources folder

    :return:
        An absolute path to the given file or folder
    """

    return make_project_path('resources', *args)

def make_results_path(*args):
    """
    Creates an absolute path to a file or folder within the results
    folder of the trackway gait analysis project using the relative path
    elements specified by the args.

    :param args:
        Zero or more relative path elements that describe a file or folder
        within the results folder

    :return:
        An absolute path to the given file or folder
    """

    return make_project_path('results', *args)

class LimbProperty(object):
    """
    A class that describes an attribute with potentially unique values for each
    limb within the quadrupedal system.
    """

    # The keys for each of the limbs
    LIMB_KEYS = [
        'left_pes',
        'right_pes',
        'left_manus',
        'right_manus' ]

    # A lookup hash between the short-format and long-format keys for each of
    # the limbs
    LIMB_KEY_LOOKUP = {
        'lp': 'left_pes',
        'rp': 'right_pes',
        'lm': 'left_manus',
        'rm': 'right_manus'
    }

    def __init__(self, **kwargs):
        self.left_pes = kwargs.get('left_pes')
        self.right_pes = kwargs.get('right_pes')
        self.left_manus = kwargs.get('left_manus')
        self.right_manus = kwargs.get('right_manus')

    def get(self, key, default = None):
        """
        Retrieve the value for the limb specified by the key

        :param key:
            The limb key for which to retrieve the value.

        :param default:
            The value returned if the value stored in the limb property is
            None.

        :return:
            The value, or its default, for the specified limb.
        """

        out = getattr(self, key)
        if out is None:
            return default

    def set(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        setattr(self, key, value)
        return self

    def assign(
            self, left_pes = None, right_pes = None, left_manus = None,
            right_manus = None):
        """
        Sets the values for each of the limb properties in the arguments list
        with a non-None value.

        :param left_pes:
        :param right_pes:
        :param left_manus:
        :param right_manus:
        :return:
        """

        if left_pes is not None:
            self.left_pes = left_pes

        if right_pes is not None:
            self.right_pes = right_pes

        if left_manus is not None:
            self.left_manus = left_manus

        if right_manus is not None:
            self.right_manus = right_manus

        return self

    def items(self):
        """

        :return:
        """

        return (
            ('left_pes', self.left_pes),
            ('right_pes', self.right_pes),
            ('left_manus', self.left_manus),
            ('right_manus', self.right_manus) )

    def values(self):
        """

        :return:
            A list containing the limb-ordered values of
        """
        return [
            self.left_pes,
            self.right_pes,
            self.left_manus,
            self.right_manus ]

    def toDict(self):
        """
        Converts the

        :return:
            A dictionary with the keys and values of the LimbProperty
        """

        return dict(
            left_pes=self.left_pes,
            right_pes=self.right_pes,
            left_manus=self.left_manus,
            right_manus=self.right_manus )
