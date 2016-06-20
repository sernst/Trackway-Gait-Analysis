import json


class Event(object):
    """

    """


    def __init__(self, time = 0.0, index = -1, value = None):
        self.time = time
        self.index = index
        self.value = value

    def clone(self):
        """

        :return:
        """

        try:
            value = self.value.clone()
        except Exception as err:
            try:
                value = json.loads(json.dumps(self.value))
            except Exception:
                value = self.value

        return Event(
            time=self.time,
            index=self.index,
            value=value
        )

    def serialize(self):
        """

        :return:
        """

        try:
            value = self.value.serialize()
        except Exception as err:
            value = self.value

        return dict(
            time=self.time,
            index=self.index,
            value=value
        )
