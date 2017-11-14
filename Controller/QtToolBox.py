# Under MIT License, see LICENSE.txt

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from Controller.DrawingObject import Color
from Controller.FieldController import FieldController

__author__ = 'RoboCupULaval'


class QtToolBox:
    """ QToolBox regroupe tous les dessins primitifs disponiblent dans Qt dans le but de facilité la création
        de dessins plus complexes."""
    line_style = {'SolidLine': Qt.SolidLine,
                  'DashLine': Qt.DashLine,
                  'DashDotLine': Qt.DashDotDotLine,
                  'DotLine': Qt.DotLine
                  }

    font_style = {'Arial': 'SansSerif',
                  'Courier New': 'TypeWriter',
                  'Verdana': 'Serif'}

    field_ctrl = FieldController()

    @staticmethod
    def create_font(style='Arial', width=10, is_bold=False, is_italic=False):
        font = QtGui.QFont()
        font.setFamily(QtToolBox.font_style[style])
        font.setBold(is_bold)
        font.setItalic(is_italic)
        font.setPixelSize(width)
        return font

    @staticmethod
    def create_pen(color=Color.BLACK, style='SolidLine', width=1, is_hide=False):
        """ Génère un pinceau avec les paramètres entrants """
        qt_pen = QtGui.QPen()
        if not is_hide:
            qt_pen.setWidth(width)
            qt_pen.setStyle(QtToolBox.line_style[style])
            qt_pen.setColor(QtGui.QColor(*color))
        else:
            qt_pen.setStyle(Qt.NoPen)
        return qt_pen

    @staticmethod
    def create_brush(color=Color.BLACK, is_visible=True):
        """ Génère un brosse avec les paramètres entrants """
        if is_visible:
            return QtGui.QBrush(QtGui.QColor(*color))
        else:
            return Qt.NoBrush

    @staticmethod
    def create_line(pst_start, pst_end, pen):
        """ Génère une ligne avec les paramètres entrants """
        qt_line = QtGui.QGraphicsLineItem(pst_start[0], pst_start[1], pst_end[0], pst_end[1])
        qt_line.setPen(pen)
        return qt_line

    @staticmethod
    def create_rect(pst_x, pst_y, width, height, pen=None, is_fill=False, brush=None, opacity=1):
        """ Génère un rectangle avec les paramètres entrants """
        qt_rect_item = QtGui.QGraphicsRectItem(pst_x, pst_y, width, height)
        if pen is not None:
            qt_rect_item.setPen(pen)
        if is_fill and brush is not None:
            qt_rect_item.setBrush(brush)
        qt_rect_item.setOpacity(opacity)
        return qt_rect_item

    @staticmethod
    def create_ellipse_item(pst_x, pst_y, width, height, pen=None, is_fill=False, brush=None, opacity=1):
        """ Génère une ellipse avec les paramètres entrants """
        qt_ellipse = QtGui.QGraphicsEllipseItem(pst_x, pst_y, width, height)
        if pen is not None:
            qt_ellipse.setPen(pen)
        if is_fill and brush is not None:
            qt_ellipse.setBrush(brush)
        qt_ellipse.setOpacity(opacity)
        return qt_ellipse
