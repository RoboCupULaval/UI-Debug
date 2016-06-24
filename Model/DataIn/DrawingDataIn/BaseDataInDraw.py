# Under MIT License, see LICENSE.txt

from Controller.BaseQtObject import BaseQtObject
from Model.DataIn.DataInObject import DataInObject

__author__ = 'RoboCupULaval'


class BaseDataInDraw(DataInObject):
    """ Données entrantes pour les paquets de données pour dessiner """
    line_style_allowed = BaseQtObject.line_style_allowed

    def __init__(self, data_in):
        DataInObject.__init__(self, data_in)
        self.data = data_in['data']

    @staticmethod
    def _colorRGB_is_valid(color):
        """ Vérifie si une couleur RGB est valide """
        try:
            assert isinstance(color, tuple)
            assert len(color) == 3
            for value in color:
                assert 0 <= value <= 255
            return True
        except AssertionError:
            return False

    @staticmethod
    def _style_is_valid(style):
        """ Vérifie si le style de ligne est valide """
        try:
            assert style in BaseDataInDraw.line_style_allowed
            return True
        except AssertionError:
            return False

    @staticmethod
    def _point_is_valid(point):
        """ Vérifie si un point est valide """
        try:
            assert isinstance(point, tuple)
            assert len(point) == 2
            for value in point:
                assert isinstance(value, int)
            return True
        except AssertionError:
            return False
