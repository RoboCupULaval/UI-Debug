# Under MIT License, see LICENSE.txt

from Model.DataIn.DataInObject import FormatPackageError
from Model.DataIn.DrawingDataIn.BaseDataInDraw import BaseDataInDraw

__author__ = 'RoboCupULaval'


class DrawTextDataIn(BaseDataInDraw):
    def __init__(self, data_in):
        BaseDataInDraw.__init__(self, data_in)
        self._format_data()

    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        try:
            assert isinstance(self.data, dict),\
                "data: {} n'est pas un dictionnaire.".format(type(self.data))
            keys = self.data.keys()

            assert 'position' in keys, \
                "data['position'] n'existe pas."
            assert self._point_is_valid(self.data['position']), \
                "data['position']: {} devrait être un point valide.".format(self.data['position'])
            assert 'text' in keys, \
                "data['text'] n'existe pas."
            assert isinstance(self.data['text'], str), \
                "data['text']: {} devrait être un string.".format(type(self.data['text']))

        except Exception as e:
            raise FormatPackageError('{}: {}'.format(type(self).__name__, e))

    def _check_optional_data(self):
        """ Vérifie les données optionnelles """
        keys = self.data.keys()
        try:
            if 'size' in keys:
                assert isinstance(self.data['size'], int), \
                    "data['size']: {} devrait être un int.".format(type(self.data['size']))
                assert self.data['size'] > 0, \
                    "data['size']: {} devrait être suppérieur à 0.".format(self.data['size'])
            else:
                self.data['size'] = 10

            if 'color' in keys:
                assert self._colorRGB_is_valid(self.data['color']), \
                    "data['color']: {} n'est pas une couleur valide.".format(self.data['color'])
            else:
                self.data['color'] = (0, 0, 0)

            if 'has_bold' in keys:
                assert isinstance(self.data['has_bold'], bool), \
                    "data['has_bold']: {} devrait être un bool.".format(type(self.data['has_bold']))
            else:
                self.data['has_bold'] = False

            if 'has_italic' in keys:
                assert isinstance(self.data['has_italic'], bool), \
                    "data['has_italic']: {} devrait être un bool.".format(type(self.data['has_italic']))
            else:
                self.data['has_italic'] = False

            if 'font' in keys:
                assert isinstance(self.data['font'], str), \
                    "data['font']: {} devrait être un string.".format(self.data['font'])
                assert self.data['font'] in {'Arial', 'Courier New', 'Verdana'}, \
                    "data['font']: {} devrait être un Arial | Courier New | Verdana.".format(self.data['font'])
            else:
                self.data['font'] = 'Arial'

            if 'align' in keys:
                assert isinstance(self.data['align'], str), \
                    "data['align']: {} devrait être un string.".format(self.data['align'])
                assert self.data['align'] in {'Right', 'Left', 'Center'}, \
                    "data['align']: {} devrait être un Right | Left | Center.".format(self.data['align'])
            else:
                self.data['align'] = 'Right'

            if 'timeout' in keys:
                assert self.data['timeout'] >= 0, \
                    "data['timeout']: {} n'est pas valide.".format(self.data['timeout'])
            else:
                self.data['timeout'] = 0

        except Exception as e:
            raise FormatPackageError('{}: {}'.format(type(self).__name__, e))

    @staticmethod
    def get_type():
        return 3008
