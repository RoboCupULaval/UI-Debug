# Under MIT License, see LICENSE.txt

from datetime import datetime

__author__ = 'RoboCupULaval'
__version__ = '1.0'


class DataIn:
    def __init__(self, name, type, version=__version__, link=None):
        try:
            self.package_is_valid(name, version, type, link)
        except AssertionError:
            raise FormatPackageError

        self.name = name
        self.type = type
        self.link = link
        self.time = datetime.now()

    @staticmethod
    def package_is_valid(name, version, type, link):
        try:
            assert isinstance(name, str)
            assert version == __version__
            assert 0 <= type < 7000
            assert link is None or 0 <= link <= 11
            return True
        except AssertionError:
            return False

    def get_time(self):
        return self.time


class FormatPackageError(BaseException):
    pass
