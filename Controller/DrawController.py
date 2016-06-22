# Under MIT License, see LICENSE.txt

from PyQt4.QtGui import QColor
from PyQt4.QtGui import QPen
from PyQt4.QtGui import QGraphicsLineItem
from PyQt4.QtCore import Qt

__author__ = 'RoboCupULaval'


class DrawController:
    _line_style_allowed = {'SolidLine': Qt.SolidLine,
                           'DashLine': Qt.DashLine,
                           'DashDotLine': Qt.DashDotDotLine,
                           'DotLine': Qt.DotLine,
                           }

    def __init__(self):
        pass

    def get_qt_draw_object(self, data_draw):
        if data_draw.type == 3001:
            # Configuration du pinceau
            pen = QPen()
            pen.setStyle(self._line_style_allowed[data_draw.data['style']])
            pen.setWidth(data_draw.data['width'])
            r, g, b = data_draw.data['color']
            pen.setColor(QColor(r, g, b))

            # Création de l'objet
            x1, y1 = data_draw.data['start']
            x2, y2 = data_draw.data['end']
            qt_obj = QGraphicsLineItem(x1, y1, x2, y2)
            qt_obj.setPen(pen)
            return qt_obj
        else:
            raise NotImplemented()