# Under MIT License, see LICENSE.txt

from Model.DataModel.DataObject import catch_format_error
from Model.DataModel.SendingData.BaseDataSending import BaseDataSending

__author__ = 'RoboCupULaval'


class SendingTarget(BaseDataSending):
    def __init__(self, data_in=None):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data: {} n'est pas un dictionnaire.".format(type(self.data))
        keys = self.data.keys()
        assert 'target' in keys, \
            "data['target'] n'existe pas."
        assert self._point_is_valid(self.data['target']), \
            "data['target']: {} n'est pas un point valide (int, int)".format(type(self.data['target']))
        assert 'id' in keys, \
            "data['id'] n'existe pas."
        assert isinstance(self.data['id'], int), \
            "data['id']: {} n'a pas le format attendu (int)".format(type(self.data['id']))

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_default_data_dict():
        """ Retourne une dictionnaire de données par défaut """
        return dict(zip(['target', 'id'],
                        [(0, 0), 0]))

    @staticmethod
    def get_type():
        return 5003
