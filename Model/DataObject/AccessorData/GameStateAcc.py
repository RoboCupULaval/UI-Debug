# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.AccessorData.BaseDataAccessor import BaseDataAccessor

__author__ = 'RoboCupULaval'


class GameStateAcc(BaseDataAccessor):
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data n'est pas un dictionnaire."

    @catch_format_error
    def _check_optional_data(self):
        keys = self.data.keys()
        if 'yellow' in keys:
            assert isinstance(self.data['yellow'], str), \
                "data['yellow']: {} n'a pas le format attendu (str)".format(type(self.data['yellow']))
        if 'blue' in keys:
            assert isinstance(self.data['blue'], str), \
                "data['blue']: {} n'a pas le format attendu (str)".format(type(self.data['blue']))

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['yellow', 'blue'],
                        ['None', 'None']))

    @staticmethod
    def get_type():
        return 1003


