# Under MIT License, see LICENSE.txt

from datetime import date

from Model.DataModel.DataObject import catch_format_error
from Model.DataModel.LoggingData.BaseDataLog import BaseDataLog

__author__ = 'RoboCupULaval'


class LoggingData(BaseDataLog):
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data: {} n'est pas un dictionnaire.".format(type(self.data))

    @catch_format_error
    def _check_optional_data(self):
        pass

    def __str__(self):
        message = ''
        message += '<{}> '.format(date.strftime(self.time, "%H:%M:%S"))
        message += '"{}": Données multiples:\n'.format(self.name)
        for key, item in sorted(self.data.items()):
            message += '{} = {}'.format(key, item) + '\n'
        return message[:-1]

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['data'],
                        ['None']))

    @staticmethod
    def get_type():
        return 1


