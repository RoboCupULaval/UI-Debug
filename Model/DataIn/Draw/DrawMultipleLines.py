# Under MIT License, see LICENSE.txt

from Model.DataIn.DataInDraw import DataInDraw
from Model.DataIn.DataIn import FormatPackageError

__author__ = 'RoboCupULaval'


class DrawMultipleLines(DataInDraw):
    def __init__(self, name, type, data):
        DataInDraw.__init__(self, name, type, data)
        self._class_type = 3002

    def format_data(self):
        """ Vérifie les données et complète les données manquantes avec des valeurs par défauts """
        try:
            if self.type == self._class_type:
                keys = self.data.keys()
                assert 'start' in keys
                assert self._point_is_valid(self.data['start'])
                assert 'end' in keys
                assert self._point_is_valid(self.data['end'])
                if 'color' in keys:
                    assert self._colorRGB_is_valid(self.data['color'])
                else:
                    self.data['color'] = (0, 0, 0)

                if 'width' in keys:
                    assert 0 < self.data['width']
                else:
                    self.data['width'] = 2

                if 'style' in keys:
                    assert self.data['style'] in self._line_style_allowed
                else:
                    self.data['style'] = 'SolidLine'

                if 'timeout' in keys:
                    assert self.data['timeout'] <= 0
                else:
                    self.data['timeout'] = 0

        except AssertionError:
            raise FormatPackageError('Les données du paquet ne sont pas valides.')


