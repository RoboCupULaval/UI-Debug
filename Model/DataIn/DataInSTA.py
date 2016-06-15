# Under MIT License, see LICENSE.txt

from .DataIn import DataIn

__author__ = 'RoboCupULaval'


class DataInSTA(DataIn):
    def __init__(self, name, type, data):
        DataIn.__init__(self, name, type, data)
        if not self.data_is_valid(name, type, data):
            raise AttributeError()

    @staticmethod
    def data_is_valid(name, type, data):
        try:
            return True

            # TODO : Vérification du paquet
            # DataIn.package_is_valid(name, type)
            assert 'T' in data.keys()
            assert data['T'] is not None
            assert isinstance(data['T'], list)
            for value in data['T']:
                assert isinstance(value, str)
            return True
        except (AssertionError, NotImplemented):
            return False

    def get_tactics(self):
        return sorted(self.data['T'])

    def get_strats(self):
        return sorted(self.data['S'])