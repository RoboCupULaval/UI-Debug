# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.AccessorData.BaseDataAccessor import BaseDataAccessor

__author__ = 'RoboCupULaval'


class RobotStateAcc(BaseDataAccessor):
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
            for id in self.data[team].keys():
                assert isinstance(id, int), \
                    "data[{}][{}]: {} n'a pas le format attendu (int)".format(team, id, type(id))
                assert 0 <= id <= 5, \
                    "data[{}][{}]: {} doit être compris entre 0 et 5".format(team, id, id)
                for state in self.data[team][id]:
                    assert isinstance(state, str), \
                        "data[{}][{}]: {} n'a pas le format attendu (str)".format(team, id, state)
                    assert state in {'target', 'action', 'tactic'}, \
                        "data[{}][{}]: {} devrait avoir la valeur suivante ('target' | 'action' | 'tactic')".format(team, id, state)
                    if state == 'target':
                        assert self._point_is_valid(self.data[team][id][state]), \
                            "data[{}][{}][{}]: {} n'est pas un point valide".format(team, id, state, self.data[team][id][state])
                    else:
                        assert isinstance(self.data[team][id][state], str), \
                            "data[{}][{}][{}]: {} n'a pas le format attendu (str)".format(team, id, state, type(self.data[team][id][state]))

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['yellow', 'blue'],
                        [dict(), dict()]))

    @staticmethod
    def get_type():
        return 1002


