# Under MIT License, see LICENSE.txt

from Model.DataIn.DataInObject import FormatPackageError
from Model.DataIn.AccessorDataIn.BaseDataAccessor import BaseDataAccessor

__author__ = 'RoboCupULaval'


class StratGeneralAcc(BaseDataAccessor):
    def __init__(self, data_in):
        BaseDataAccessor.__init__(self, data_in)
        self._format_data()

    def _check_obligatory_data(self):
        try:
            assert isinstance(self.data, dict), \
                "data: {} n'est pas un dictionnaire.".format(type(self.data))
        except Exception as e:
            raise FormatPackageError('{}: {}'.format(self.__name__, e))

    def _check_optional_data(self):
        try:
            keys = self.data.keys()
            if 'strategy' in keys:
                assert isinstance(self.data['strategy'], list)
                for value in self.data['strategy']:
                    assert isinstance(value, str)

            if 'tactic' in keys:
                assert isinstance(self.data['tactic'], list)
                for value in self.data['tactic']:
                    assert isinstance(value, str)

            if 'action' in keys:
                assert isinstance(self.data['action'], list)
                for value in self.data['action']:
                    assert isinstance(value, str)

        except Exception as e:
            raise FormatPackageError('{}: {}'.format(self.__name__, e))

    @staticmethod
    def get_type():
        return 1001


