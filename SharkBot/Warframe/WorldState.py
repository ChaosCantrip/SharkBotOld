from datetime import datetime


class WorldState:

    def __init__(self, data: dict):
        self._data = data
        self._timestamp = datetime.utcnow()

