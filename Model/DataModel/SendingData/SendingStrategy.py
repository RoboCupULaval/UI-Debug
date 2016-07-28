# Under MIT License, see LICENSE.txt

from Model.DataModel.DataObject import catch_format_error
from Model.DataModel.SendingData.BaseDataSending import BaseDataSending

__author__ = 'RoboCupULaval'


class SendingStrategy(BaseDataSending):
    def __init__(self, data_in=None):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data: {} n'est pas un dictionnaire.".format(type(self.data))
        keys = self.data.keys()
        assert 'strategy' in keys, \
            "data['strategy'] n'existe pas."
        assert isinstance(self.data['strategy'], str), \
            "data['strategy']: {} n'est pas le type attendu (str)".format(type(self.data['strategy']))

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_default_data_dict():
        """ Retourne une dictionnaire de données par défaut """
        return dict(zip(['strategy'],
                        ['StrategyHelloWorld']))

    @staticmethod
    def get_type():
        return 5002
