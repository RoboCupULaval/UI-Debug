# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.AccessorData.BaseDataAccessor import BaseDataAccessor

__author__ = 'RoboCupULaval'


class RobotStrategicStateAcc(BaseDataAccessor):
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
            assert key in {'yellow', 'blue'}, \
                "data[{}] n'est pas une clé validee (yellow | blue)".format(key)
            assert isinstance(self.data[key], dict), \
                "data[{}]: {} n'a pas le format attendu (dict)".format(key, type(self.data[key]))

    @catch_format_error
    def _check_optional_data(self):
        for team in self.data.keys():
            for idx in self.data[team].keys():
                assert isinstance(idx, int), \
                    "data[{}][{}]: {} n'a pas le format attendu (int)".format(team, idx, type(idx))
                assert 0 <= idx <= 11, \
                    "data[{}][{}]: {} doit être compris entre 0 et 11".format(team, idx, idx)
                for state in self.data[team][idx]:
                    assert isinstance(state, str), \
                        "data[{}][{}]: {} n'a pas le format attendu (str)".format(team, idx, state)
                    assert state in {'tactic', 'state', 'role'}, \
                        "data[{}][{}]: {} devrait avoir la valeur suivante ('tactic' | 'state' | 'role')".format(team, idx, state)
                    if state == 'target':
                        assert self._point_is_valid(self.data[team][idx][state]), \
                            "data[{}][{}][{}]: {} n'est pas un point valide".format(team, idx, state, self.data[team][idx][state])
                    else:
                        assert isinstance(self.data[team][idx][state], str), \
                            "data[{}][{}][{}]: {} n'a pas le format attendu (str)".format(team, idx, state, type(self.data[team][idx][state]))

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['yellow', 'blue'],
                        [dict(), dict()]))

    @staticmethod
    def get_type():
        return 1002


