# Under MIT License, see LICENSE.txt

from Model.DataIn.DrawingDataIn.BaseDataInDraw import BaseDataInDraw
from Model.DataIn.DataInObject import FormatPackageError

__author__ = 'RoboCupULaval'


class DrawInfluenceMapDataIn(BaseDataInDraw):
    def __init__(self, data_in):
        BaseDataInDraw.__init__(self, data_in)
        self._format_data()

    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        try:
            assert isinstance(self.data, dict), \
                "data: {} n'est pas un dictionnaire.".format(type(self.data))
            keys = self.data.keys()
            assert 'field_data' in keys, \
                "data['field_data'] n'existe pas."
            assert isinstance(self.data['field_data'], list), \
                "data['field_data']: {} n'a pas le format attendu (list)".format(type(self.data['field_data']))
            for nb_line, line in enumerate(self.data['field_data']):
                assert isinstance(line, list), \
                "data['field_data'][{}]: {} n'a pas le format attendu (list)".format(nb_line, type(line))
                for nb_col, case in enumerate(line):
                    assert isinstance(case, int), \
                        "data['field_data'][{}][{}]: {} n'a pas le format attendu (int)" \
                        "".format(nb_line, nb_col, type(case))
        except Exception as e:
            raise FormatPackageError('{}: {}'.format(type(self).__name__, e))

    def _check_optional_data(self):
        # TODO - InfluenceMap.checkOptional_data
        try:
            keys = self.data.keys()
            if 'dimension' in keys:
                assert self._point_is_valid(self.data['dimension'])
            else:
                self.data['dimension'] = len(self.data['field_data'][0]), len(self.data['field_data'])

            if 'hotest_numb' in keys:
                assert isinstance(self.data['hotest_numb'], int)
            else:
                maxi = 0
                for line in self.data['field_data']:
                    tmp_max = max(line)
                    if tmp_max > maxi:
                        maxi = tmp_max
                self.data['hotest_numb'] = maxi

            if 'coldest_numb' in keys:
                assert isinstance(self.data['coldest_numb'], int)
            else:
                mini = 10000000
                for line in self.data['field_data']:
                    tmp_min = min(line)
                    if tmp_min < mini:
                        mini = tmp_min
                self.data['coldest_numb'] = mini

        except Exception as e:
            raise FormatPackageError('{}: {}'.format(type(self).__name__, e))

    @staticmethod
    def get_type():
        return 3007
