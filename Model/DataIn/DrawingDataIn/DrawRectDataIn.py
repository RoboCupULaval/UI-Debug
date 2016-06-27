# Under MIT License, see LICENSE.txt

from Model.DataIn.DataInObject import FormatPackageError
from Model.DataIn.DrawingDataIn.BaseDataInDraw import BaseDataInDraw

__author__ = 'RoboCupULaval'


class DrawRectDataIn(BaseDataInDraw):
    def __init__(self, data_in):
        BaseDataInDraw.__init__(self, data_in)
        self._format_data()

    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        try:
            assert isinstance(self.data, dict),\
                "data: {} n'est pas un dictionnaire.".format(type(self.data))
            keys = self.data.keys()

            assert 'top_left' in keys, \
                "data['top_left'] n'existe pas."
            assert self._point_is_valid(self.data['top_left']), \
                "data['top_left']: {} n'est pas un point valide.".format(self.data['top_left'])

            assert 'bottom_right' in keys, \
                "data['bottom_right'] n'existe pas."
            assert self._point_is_valid(self.data['bottom_right']), \
                "data['bottom_right']: {} n'est pas un point valide.".format(self.data['bottom_right'])
        except Exception as e:
            raise FormatPackageError('{}: {}'.format(type(self).__name__, e))

    def _check_optional_data(self):
        """ Vérifie les données optionnelles """
        keys = self.data.keys()
        try:
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

            if 'width' in keys:
                assert isinstance(self.data['width'], int), \
                    "data['width']: {} n'est pas du bon type (int)".format(type(self.data['width']))
            else:
                self.data['width'] = 2

            if 'style' in keys:
                assert self.data['style'] in self.line_style_allowed, \
                    "data['style']: {} n'est pas une style valide".format(self.data['style'])
            else:
                self.data['style'] = 'SolidLine'

            if 'timeout' in keys:
                assert self.data['timeout'] <= 0, \
                    "data['timeout']: {} n'est pas valide.".format(self.data['timeout'])
            else:
                self.data['timeout'] = 0
        except Exception as e:
            raise FormatPackageError('{}: {}'.format(type(self).__name__, e))

    @staticmethod
    def get_type():
        return 3006
