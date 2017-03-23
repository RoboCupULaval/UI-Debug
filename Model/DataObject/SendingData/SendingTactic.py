# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.SendingData.BaseDataSending import BaseDataSending

__author__ = 'RoboCupULaval'


class SendingTactic(BaseDataSending):
    def __init__(self, data_in=None):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data: {} n'est pas un dictionnaire.".format(type(self.data))
        keys = self.data.keys()
        assert 'tactic' in keys, \
            "data['tactic'] n'existe pas."
        assert isinstance(self.data['tactic'], str), \
            "data['tactic']: {} n'est pas le type attendu (str)".format(type(self.data['tactic']))
        assert 'id' in keys, \
            "data['id'] n'existe pas."
        assert isinstance(self.data['id'], int), \
            "data['id']: {} n'a pas le format attendu (int)".format(type(self.data['id']))

    @catch_format_error
    def _check_optional_data(self):
        keys = self.data.keys()
        if 'target' in keys:
            assert self._point_is_valid(self.data['target']), \
                "data['target']: {} n'est pas un point valide (int, int)".format(self.data['target'])
        else:
            self._data['data']['target'] = 0, 0

        if 'goal' in keys:
            assert self._point_is_valid(self.data['goal']), \
                "data['goal']: {} n'est pas un point valide (int, int)".format(self.data['goal'])
        else:
            self._data['data']['goal'] = 0, 0

        if 'args' in keys:
            assert isinstance(self.data['args'], list), \
                "data['args'] n'a pas le format attendu (list(str))"
        else:
            self._data['data']['args'] = []

    @staticmethod
    def get_default_data_dict():
        """ Retourne une dictionnaire de données par défaut """
        return dict(zip(['tactic', 'id'],
                        ['TacticHelloWorld', 0]))

    @staticmethod
    def get_type():
        return 5003
