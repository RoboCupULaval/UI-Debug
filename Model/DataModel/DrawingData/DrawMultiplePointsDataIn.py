# Under MIT License, see LICENSE.txt

from Model.DataModel.DataObject import catch_format_error
from Model.DataModel.DrawingData.BaseDataDraw import BaseDataDraw

__author__ = 'RoboCupULaval'


class DrawMultiplePointsDataIn(BaseDataDraw):
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        assert isinstance(self.data, dict),\
            "data: {} n'est pas un dictionnaire.".format(type(self.data))
        keys = self.data.keys()

        assert 'points' in keys, \
            "data['points'] n'existe pas."
        assert isinstance(self.data['points'], list), \
            "data['points']: {} n'a pas le format attendu (list)".format(type(self.data['points']))
        for i, point in enumerate(self.data['points']):
            assert self._point_is_valid(point), \
                "data['points'][{}]: {} n'est pas un point valide.".format(i, type(self.data['points']))

    @catch_format_error
    def _check_optional_data(self):
        """ Vérifie les données optionnelles """
        keys = self.data.keys()
        if 'color' in keys:
            assert self._colorRGB_is_valid(self.data['color']), \
                "data['color']: {} n'est pas une couleur valide.".format(self.data['color'])
        else:
            self.data['color'] = (0, 0, 0)

        if 'width' in keys:
            assert isinstance(self.data['width'], int), \
                "data['width']: {} n'est pas du bon type (int)".format(type(self.data['width']))
        else:
            self.data['width'] = 3

        if 'timeout' in keys:
            assert self.data['timeout'] >= 0, \
                "data['timeout']: {} n'est pas valide.".format(self.data['timeout'])
        else:
            self.data['timeout'] = 0

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['points'],
                        [[(x * 100, -250) for x in range(5)]]))

    @staticmethod
    def get_type():
        return 3005
