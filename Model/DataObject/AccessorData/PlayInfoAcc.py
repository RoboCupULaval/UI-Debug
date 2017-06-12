# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.AccessorData.BaseDataAccessor import BaseDataAccessor

__author__ = 'RoboCupULaval'


class PlayInfoAcc(BaseDataAccessor):
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data: {} n'est pas un dictionnaire.".format(type(self.data))
        keys = self.data.keys()

        for key in keys:
            assert isinstance(key, str), \
                "data[{}]: {} la clé n'a pas le format attendu (str)".format(key, type(key))
            assert key in {'referee', 'referee_team', 'auto_play', 'auto_flag'}, \
                "data[{}] n'est pas une clé validee".format(key)
            assert isinstance(self.data[key], dict) or isinstance(self.data[key], bool), \
                "data[{}]: {} n'a pas le format attendu (dict | bool)".format(key, type(self.data[key]))

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_default_data_dict():
        return dict()

    @staticmethod
    def get_type():
        return 1005


