# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.SendingData.BaseDataSending import BaseDataSending

__author__ = 'RoboCupULaval'


class SendingAutoPlay(BaseDataSending):
    def __init__(self, data_in=None):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        pass

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_default_data_dict():
        """ Retourne une dictionnaire de données par défaut """
        return {'status': False}

    @staticmethod
    def get_type():
        return 5008
