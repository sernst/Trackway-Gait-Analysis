
import os

MY_PATH = os.path.abspath(os.path.dirname(__file__))

def make_project_path(*args):
    """

    :param args:
    :return:
    """
    return os.path.abspath(os.path.join(MY_PATH, '..', '..', *args))

def make_resource_path(*args):
    """

    :param args:
    :return:
    """
    return make_project_path('resources', *args)

def make_results_path(*args):
    """

    :param args:
    :return:
    """

    return make_project_path('results', *args)

class LimbProperty(object):

    LIMB_KEYS = [
        'left_pes',
        'right_pes',
        'left_manus',
        'right_manus' ]

    def __init__(self, **kwargs):
        self.left_pes = kwargs.get('left_pes')
        self.right_pes = kwargs.get('right_pes')
        self.left_manus = kwargs.get('left_manus')
        self.right_manus = kwargs.get('right_manus')

    def get(self, key, default = None):
        """

        :param key:
        :param default:
        :return:
        """
        return getattr(self, key, default)

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
        :return:
            A dictionary with the keys and values of the LimbProperty
        """

        return dict(
            left_pes=self.left_pes,
            right_pes=self.right_pes,
            left_manus=self.left_manus,
            right_manus=self.right_manus )
