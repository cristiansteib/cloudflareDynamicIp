
class FileCache:

    def __init__(self, path=''):
        self._directory = path
        self._data = dict()

    def _save_value_on_disk(self, key, value):
        file = open(self._directory + key, mode='w')
        file.write(value)
        file.close()

    def _retrieve_value_from_disk(self, key):
        value = None
        try:
            file = open(self._directory + key, mode='r')
            value = file.read()
            file.close()
        except FileNotFoundError:
            pass
        return value

    def set(self, key, value):
        old_value = self._data.get(key, None)
        if old_value != value:
            self._data[key] = str(value).strip()
            self._save_value_on_disk(key, self._data[key])

    def get(self, key):
        value = self._data.get(key, None)
        if value is not None:
            return value
        self._data[key] = self._retrieve_value_from_disk(key)
        return self._data[key]