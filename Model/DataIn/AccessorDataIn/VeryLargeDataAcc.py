# Under MIT License, see LICENSE.txt

from Model.DataIn.AccessorDataIn.BaseDataAccessor import BaseDataAccessor
from Model.DataIn.DataInObject import catch_format_error

__author__ = 'RoboCupULaval'


class VeryLargeDataAcc(BaseDataAccessor):
    __waiting_pieces = dict()

    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    def store(self):
        if self.data['id'] not in VeryLargeDataAcc.__waiting_pieces:
            VeryLargeDataAcc.__waiting_pieces[self.data['id']] = dict()
        VeryLargeDataAcc.__waiting_pieces[self.data['id']][self.data['piece_number']] = self.data['binary']

    @catch_format_error
    def rebuild(self):
        if len(VeryLargeDataAcc.__waiting_pieces[self.data['id']].keys()) == self.data['total_pieces']:
            bin_rebuilt = b''
            for i in range(1, self.data['total_pieces'] + 1):
                bin_rebuilt += VeryLargeDataAcc.__waiting_pieces[self.data['id']][i]
            return bin_rebuilt
        else:
            return None

    @catch_format_error
    def _check_obligatory_data(self):
        assert isinstance(self.data, dict), \
            "data: {} n'est pas un dictionnaire.".format(type(self.data))

        keys = self.data.keys()
        assert 'id' in keys, \
            "data['id'] n'existe pas."
        assert isinstance(self.data['id'], str), \
            "data['id']: {} n'a pas le format attendu str".format(type(self.data['id']))

        assert 'total_pieces' in keys, \
            "data['total_pieces'] n'existe pas."
        assert isinstance(self.data['total_pieces'], int), \
            "data['total_pieces']: {} n'a pas le format attendu int".format(type(self.data['total_pieces']))
        assert self.data['total_pieces'] > 0, \
            "data['total_pieces']: {} doit être > 0".format(self.data['total_pieces'])

        assert 'piece_number' in keys, \
            "data['piece_number'] n'existe pas."
        assert isinstance(self.data['piece_number'], int), \
            "data['piece_number']: {} n'a pas le format attendu int".format(type(self.data['piece_number']))
        assert 0 < self.data['piece_number'] <= self.data['total_pieces'], \
            "data['piece_number']: {} doit être compris entre 0 et {} inclu".format(self.data['piece_number'],
                                                                                    self.data['total_pieces'])

        assert 'binary' in keys, \
            "data['binary'] n'existe pas."
        assert isinstance(self.data['binary'], bytes), \
            "data['binary']: {} n'a pas le format attendu bytes".format(type(self.data['binary']))

    @catch_format_error
    def _check_optional_data(self):
        pass

    @staticmethod
    def get_type():
        return 2000
