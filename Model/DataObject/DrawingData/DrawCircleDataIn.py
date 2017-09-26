# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.DrawingData.BaseDataDraw import BaseDataDraw

__author__ = 'RoboCupULaval'


class DrawCircleDataIn(BaseDataDraw):
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        assert isinstance(self.data, dict),\
            "data: {} n'est pas un dictionnaire.".format(type(self.data))
        keys = self.data.keys()
        assert 'center' in keys, \
            "data['center'] n'existe pas."
        assert self._point_is_valid(self.data['center']), \
            "data['center']: {} n'est pas un point valide.".format(self.data['center'])
        assert 'radius' in keys, \
            "data['radius'] n'existe pas."
        assert isinstance(self.data['radius'], (int, float)), \
            "data['radius']: {} n'a pas une taille valide (int)".format(type(self.data['radius']))
        assert 0 < self.data['radius'], \
            "data['radius']: {} n'a pas une taille valide (0 < radius)".format(type(self.data['radius']))

    @catch_format_error
    def _check_optional_data(self):
        """ Vérifie les données optionnelles """
        keys = self.data.keys()
        if 'color' in keys:
            assert self._colorRGB_is_valid(self.data['color']), \
                "data['color']: {} n'est pas une couleur valide.".format(self.data['color'])
        else:
            self.data['color'] = (0, 0, 0)

        if 'is_fill' in keys:
            assert isinstance(self.data['is_fill'], bool), \
                "data['is_fill']: {} n'est pas du bon type (bool)".format(type(self.data['is_fill']))
        else:
            self.data['is_fill'] = False

        if 'style' in keys:
            assert self.data['style'] in self.line_style_allowed, \
                "data['style']: {} n'est pas une style valide".format(self.data['style'])
        else:
            self.data['style'] = 'SolidLine'

        if 'timeout' in keys:
            assert self.data['timeout'] >= 0, \
                "data['timeout']: {} n'est pas valide.".format(self.data['timeout'])
        else:
            self.data['timeout'] = 0

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['center', 'radius'],
                        [(0, 0), 250]))

    @staticmethod
    def get_type():
        return 3003
