# Under MIT License, see LICENSE.txt

from Model.DataIn.DataInObject import catch_format_error
from Model.DataIn.DrawingDataIn.BaseDataInDraw import BaseDataInDraw

__author__ = 'RoboCupULaval'


class DrawLineDataIn(BaseDataInDraw):
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        assert isinstance(self.data, dict),\
            "data: {} n'est pas un dictionnaire.".format(type(self.data))
        keys = self.data.keys()
        assert 'start' in keys, \
            "data['start'] n'existe pas."
        assert self._point_is_valid(self.data['start']), \
            "data['start']: {} n'est pas un point valide.".format(self.data['start'])
        assert 'end' in keys, \
            "data['end'] n'existe pas."
        assert self._point_is_valid(self.data['end']),\
            "data['end']: {} n'est pas un point valide.".format(self.data['end'])

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
            assert 0 < self.data['width'], \
                "data['width']: {} n'est pas une épaisseur valide".format(self.data['width'])
        else:
            self.data['width'] = 2

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
    def get_type():
        return 3001
