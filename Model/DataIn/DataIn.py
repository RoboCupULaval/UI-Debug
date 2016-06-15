# Under MIT License, see LICENSE.txt

from datetime import datetime

__author__ = 'RoboCupULaval'


class DataIn(object):
    def __init__(self, name, type, data):
        self.name = name
        self.type = type
        self.data = data
        self.time = datetime.now()

    @staticmethod
    def package_is_valid(name, type):
        assert isinstance(name, str)
        assert isinstance(type, int)
        assert 0 <= type <= 50

    def get_time(self):
        return self.time
