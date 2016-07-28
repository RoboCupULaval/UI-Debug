# Under MIT License, see LICENSE.txt

from Model.DataModel.DataObject import catch_format_error
from Model.DataModel.DrawingData.BaseDataDraw import BaseDataDraw

__author__ = 'RoboCupULaval'


class DrawTreeDataIn(BaseDataDraw):
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
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
            self.data['width'] = 2

        if 'timeout' in keys:
            assert self.data['timeout'] >= 0, \
                "data['timeout']: {} n'est pas valide.".format(self.data['timeout'])
        else:
            self.data['timeout'] = 0

    @staticmethod
    def get_default_data_dict():
        return dict(zip(['tree'],
                        [[((0, 0), (100, 100)),
                          ((0, 0), (100, -100))]]))

    @staticmethod
    def get_type():
        return 3009
