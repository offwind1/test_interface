
class DataAgent():
    def __init__(self):
        self._data = None

    def update(self):
        self.data = self.init_data()

    @property
    def data(self):
        if self._data is None:
            self.update()
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
