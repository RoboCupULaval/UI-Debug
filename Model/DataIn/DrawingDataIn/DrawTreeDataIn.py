# Under MIT License, see LICENSE.txt

from Model.DataIn.DataInObject import FormatPackageError
from Model.DataIn.DrawingDataIn.BaseDataInDraw import BaseDataInDraw

__author__ = 'RoboCupULaval'


class DrawTreeDataIn(BaseDataInDraw):
    def __init__(self, data_in):
        BaseDataInDraw.__init__(self, data_in)
        self._format_data()

    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        try:
            assert isinstance(self.data, dict),\
                "data: {} n'est pas un dictionnaire.".format(type(self.data))
            keys = self.data.keys()

            assert 'tree' in keys, \
                "data['tree'] n'existe pas."
            assert isinstance(self.data['tree'], list), \
                "data['tree']: {} devrait être une liste.".format(self.data['tree'])
            for i, node in enumerate(self.data['tree']):
                assert isinstance(node, tuple), \
                "data['tree'][{}]: {} devrait être un tuple.".format(i, type(node))
                assert len(node) == 2, \
                "data['tree'][{}]: {} devrait contenir 2 points.".format(i, len(node))
                for point in node:
                    assert self._point_is_valid(point), \
                    "data['tree'][{}]: {} devrait être un point valide.".format(i, point)

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

            if 'width' in keys:
                assert isinstance(self.data['width'], int), \
                    "data['width']: {} n'est pas du bon type (int)".format(type(self.data['width']))
            else:
                self.data['width'] = 2

            if 'timeout' in keys:
                assert self.data['timeout'] >= 0, \
                    "data['timeout']: {} n'est pas valide.".format(self.data['timeout'])
            else:
                self.data['timeout'] = 0

        except Exception as e:
            raise FormatPackageError('{}: {}'.format(type(self).__name__, e))

    @staticmethod
    def get_type():
        return 3009
