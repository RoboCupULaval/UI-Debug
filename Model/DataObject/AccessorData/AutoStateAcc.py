# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.AccessorData.BaseDataAccessor import BaseDataAccessor

__author__ = 'RoboCupULaval'


class AutoStateAcc(BaseDataAccessor):
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
            assert key in {'referee_cmd', 'game_stage', 'current_strategy', 'status', 'state', 'referee_team_info'}, \
                "data[{}] n'est pas une clé validee (referee_cmd | game_stage | current_strategy)".format(key)
            assert isinstance(self.data[key], str) or isinstance(self.data[key], bool) or isinstance(self.data[key], dict), \
                "data[{}]: {} n'a pas le format attendu (str, bool or dict)".format(key, type(self.data[key]))

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_default_data_dict():
        return dict()

    @staticmethod
    def get_type():
        return 1005


