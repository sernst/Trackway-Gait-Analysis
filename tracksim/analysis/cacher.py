
CACHE = dict()


def put(**kwargs):
    """

    :param kwargs:
    :return:
    """

    for key, value in kwargs.items():
        CACHE[key] = value


def fetch(key: str, default_value=None):
    """

    :param key:
    :param default_value:
    :return:
    """

    if key in CACHE:
        return CACHE[key]
