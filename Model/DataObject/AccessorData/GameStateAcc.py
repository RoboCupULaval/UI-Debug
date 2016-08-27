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
        keys = self.data.keys()

        assert 'state' in keys, \
            "data['state'] n'existe pas."
        assert isinstance(self.data['state'], str), \
            "data['state']: {} n'a pas le format attendu".format(type(self.data['state']))

        assert 'team' in keys, \
            "data['team'] n'existe pas."
        assert isinstance(self.data['team'], str), \
            "data['team']: {} n'a pas le format attendu".format(type(self.data['team']))
        assert self.data['team'].lower() in {'yellow', 'blue'}, \
            "data['team']: {} n'a pas la valeur attendue (yellow | blue)".format(self.data['team'])

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['state', 'team'],
                        ['None', 'yellow']))

    @staticmethod
    def get_type():
        return 1003


