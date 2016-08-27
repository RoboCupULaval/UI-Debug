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

        assert 'id' in keys, \
            "data['id'] n'existe pas."
        assert isinstance(self.data['id'], int), \
            "data['id']: {} n'a pas le format attendu (int)".format(type(self.data['id']))
        assert 0 <= self.data['id'] <= 5, \
            "data['id']: {} n'est pas compris entre 0 et 5".format(self.data['id'])

        assert 'team' in keys, \
            "data['team'] n'existe pas."
        assert self.data['team'].lower() in {'blue', 'yellow'}, \
            "data['team'] {} n'a pas la valeur attendue (blue | yellow)".format(self.data['team'])

    @catch_format_error
    def _check_optional_data(self):
        keys = self.data.keys()
        if 'tactic' in keys and self.data['tactic'] is not None:
            assert isinstance(self.data['tactic'], str), \
                "data['tactic']: {} n'a pas le format attendu (str)".format(type(self.data['tactic']))
        else:
            self.data['tactic'] = None

        if 'action' in keys and self.data['action'] is not None:
            assert isinstance(self.data['action'], str), \
                "data['action']: {} n'a pas le format attendu (str)".format(type(self.data['action']))
        else:
            self.data['action'] = None

        if 'target' in keys and self.data['target'] is not None:
            assert self._point_is_valid (self.data['target']), \
                "data['target']: {} n'a pas le format attendu (tuple(int, int))".format(self.data['target'])
        else:
            self.data['target'] = None

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['id', 'team', 'tactic', 'action', 'target'],
                        [0, 'Yellow', None, None, None]))

    @staticmethod
    def get_type():
        return 1002


