# Under MIT License, see LICENSE.txt

from Model.DataObject.DrawingData.BaseDataDraw import BaseDataDraw
from Model.DataObject.BaseDataObject import catch_format_error

__author__ = 'RoboCupULaval'


class DrawInfluenceMapDataIn(BaseDataDraw):
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        assert isinstance(self.data, dict), \
            "data: {} n'est pas un dictionnaire.".format(type(self.data))
        keys = self.data.keys()
        assert 'field_data' in keys, \
            "data['field_data'] n'existe pas."
        assert isinstance(self.data['field_data'], list), \
            "data['field_data']: {} n'a pas le format attendu (list)".format(type(self.data['field_data']))
        data_len = len(self.data['field_data'][0])
        for nb_line, line in enumerate(self.data['field_data']):
            assert isinstance(line, list), \
                "data['field_data'][{}]: {} n'a pas le format attendu (list)".format(nb_line, type(line))
            assert len(line) == data_len, \
                "data['field_data'][{}]: {} n'a pas une longueur uniforme ({})".format(nb_line, len(line), data_len)
            for nb_col, case in enumerate(line):
                assert isinstance(case, int), \
                    "data['field_data'][{}][{}]: {} n'a pas le format attendu (int)" \
                    "".format(nb_line, nb_col, type(case))

    @catch_format_error
    def _check_optional_data(self):
        """ Vérifie les données optionnelles """
        # TODO : Finir les messages d'erreurs
        keys = self.data.keys()
        if 'size' in keys:
            assert self._point_is_valid(self.data['size'])
            assert self.data['size'] == len(self.data['field_data'][0]), len(self.data['field_data'])
        else:
            self.data['size'] = len(self.data['field_data'][0]), len(self.data['field_data'])

        if 'focus' in keys:
            assert isinstance(self.data['focus'], tuple)
            assert len(self.data['focus']) == 4
            for i, value in enumerate(self.data['focus']):
                assert isinstance(value, int)
                assert 0 <= value
        else:
            self.data['focus'] = 0, 0, self.data['size'][0], self.data['size'][1]

        if 'hottest_numb' in keys:
            assert isinstance(self.data['hottest_numb'], int)
        else:
            maxi = 0
            for line in self.data['field_data']:
                tmp_max = max(line)
                if tmp_max > maxi:
                    maxi = tmp_max
            self.data['hottest_numb'] = maxi

        if 'hottest_color' in keys:
            assert BaseDataDraw._colorRGB_is_valid(self.data['hottest_color'])
        else:
            self.data['hottest_color'] = 255, 0, 0

        if 'coldest_numb' in keys:
            assert isinstance(self.data['coldest_numb'], int)
        else:
            mini = 10000000
            for line in self.data['field_data']:
                tmp_min = min(line)
                if tmp_min < mini:
                    mini = tmp_min
            self.data['coldest_numb'] = mini

        assert self.data['coldest_numb'] <= self.data['hottest_numb']

        if 'coldest_color' in keys:
            assert BaseDataDraw._colorRGB_is_valid(self.data['coldest_color'])
        else:
            self.data['coldest_color'] = 0, 255, 0

        if 'has_grid' in keys:
            assert isinstance(self.data['has_grid'], bool)
        else:
            self.data['has_grid'] = False

        if 'grid_color' in keys:
            assert BaseDataDraw._colorRGB_is_valid(self.data['grid_color']), \
                "'grid_color' format non valide (RGB)"
        else:
            self.data['grid_color'] = 0, 0, 0

        if 'grid_width' in keys:
            assert isinstance(self.data['grid_width'], int), "'grid_width' format non valide (int)"
            assert 0 <= self.data['grid_width'], "'grid_width' valeur non valide (0 <= grid_width)"
        else:
            self.data['grid_width'] = 0

        if 'grid_style' in keys:
            assert isinstance(self.data['grid_style'], str)
            assert self.data['grid_style'] in BaseDataDraw.line_style_allowed
        else:
            self.data['grid_style'] = 'SolidLine'

        if 'opacity' in keys:
            assert isinstance(self.data['opacity'], int)
            assert 0 <= self.data['opacity'] <= 10
        else:
            self.data['opacity'] = 10

        if 'timeout' in keys:
            assert self.data['timeout'] >= 0, \
                "data['timeout']: {} n'est pas valide.".format(self.data['timeout'])
        else:
            self.data['timeout'] = 0

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['field_data'],
                        [[[x + y for x in range(90)] for y in range(60)]]))

    @staticmethod
    def get_type():
        return 3007