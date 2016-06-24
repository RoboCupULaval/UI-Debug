# Under MIT License, see LICENSE.txt

from datetime import date

from Model.DataIn.DataInObject import FormatPackageError
from Model.DataIn.LoggingDataIn.BaseDataInLog import BaseDataInLog

__author__ = 'RoboCupULaval'


class LoggingMessage(BaseDataInLog):
    def __init__(self, data_in):
        BaseDataInLog.__init__(self, data_in)
        self._format_data()

    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        try:
            keys = self.data.keys()
            assert 'level' in keys, \
                "data['level'] n'existe pas."
            assert isinstance(self.data['level'], int), \
                "data['level']: {} n'est pas un level valide int.".format(type(self.data['level']))
            assert min(BaseDataInLog.display_type.keys()) <= self.data['level'] <= max(BaseDataInLog.display_type.keys()), \
                "data['level']: {} n'est pas un level valide 0 <= level <= 5.".format(type(self.data['level']))
            assert 'message' in keys, "data['message'] n'existe pas."
            assert isinstance(self.data['message'], str), \
                "data['message']: {} n'est pas une chaîne de caractères (str).".format(type(self.data['message']))
        except Exception as e:
            raise FormatPackageError('{}: {}'.format(self.__name__, e))

    def _check_optinal_data(self):
        """ Vérifie les données optionnelles """
        try:
            pass
        except Exception as e:
            raise FormatPackageError('{}: {}'.format(self.__name__, e))

    def __str__(self):
        message = ''
        message += '<{}> '.format(date.strftime(self.time, "%H:%M:%S"))
        message += '"{}": '.format(self.name)
        message += "<{}> ".format(self.display_type[self.data['level']])
        message += self.data['message']
        return message

    def get_message(self):
        return self.data['message']

    def get_level(self):
        return self.data['level']

    @staticmethod
    def get_type():
        return 2
