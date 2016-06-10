# Under MIT License, see LICENSE.txt

from .DataInLog import DataInLog
from .DataInSTA import DataInSTA

__author__ = 'RoboCupULaval'


class DataInFactory(object):

    @staticmethod
    def get_data(name, type, data):
        if DataInLog.data_is_valid(name, type, data):
            return DataInLog(name, type, data)
        elif DataInSTA.data_is_valid(name, type, data):
            return DataInSTA(name, type, data)
        else:
            print('')
            raise NotImplemented()
