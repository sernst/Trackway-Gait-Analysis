shared = None
report = None


class SharedCache(object):
    """

    """

    def __init__(self):
        self.data = dict()

    def put(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

        for key, value in kwargs.items():
            self.data[key] = value

    def fetch(self, key: str, default_value=None):
        """

        :param key:
        :param default_value:
        :return:
        """

        return self.data.get(key, default_value)

    def __getitem__(self, item):
        return self.data.get(item)

    def __getattr__(self, item):
        return self.data.get(item)
