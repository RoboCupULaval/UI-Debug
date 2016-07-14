# Under MIT License, see LICENSE.txt

from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QColor
from PyQt4.QtCore import QThread
from PyQt4.QtCore import QRect

from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox
from Model.DataIn.DrawingDataIn.DrawInfluenceMapDataIn import DrawInfluenceMapDataIn

__author__ = 'RoboCupULaval'


class InfluenceMapDrawing(BaseDrawingObject):
    def __init__(self, data_in):
        BaseDrawingObject.__init__(self, data_in)
        self._pixmap = None
        self._thread = QThread()
        self._thread.run = self._draw_image
        self._thread.start()


    def _draw_image(self):
        width, height = self.data['size']
        image = QImage(height, width, QImage.Format_RGB16)
        for nb_line, line in enumerate(self.data['field_data']):
            for nb_col, case in enumerate(line):
                if case > self.data['hottest_numb']:
                    case = self.data['hottest_numb']
                if case < self.data['coldest_numb']:
                    case = self.data['coldest_numb']
                rgb_value = InfluenceMapDrawing._convert_rgb_value_with_minmax(case,
                                                                               self.data['coldest_numb'],
                                                                               self.data['hottest_numb'],
                                                                               self.data['coldest_color'],
                                                                               self.data['hottest_color'])
                image.setPixel(nb_line, nb_col, QColor(*rgb_value).rgb())
        self._pixmap = image

    def draw(self, painter):
        if self._pixmap is not None and self.isVisible():
            x, y = QtToolBox.field_ctrl.get_top_left_to_screen()
            width = QtToolBox.field_ctrl.size[0] * QtToolBox.field_ctrl.ratio_screen
            height = QtToolBox.field_ctrl.size[1] * QtToolBox.field_ctrl.ratio_screen
            painter.drawImage(QRect(x, y, width, height),
                              self._pixmap.mirrored(horizontal=QtToolBox.field_ctrl.is_x_axe_flipped,
                       vertical=QtToolBox.field_ctrl.is_y_axe_flipped))

    @staticmethod
    def _convert_rgb_value_with_minmax(value, value_min, value_max, rgb_min, rgb_max):
        """ Retourne une valeur RGB pour un dégradé de couleur en fonction de la valeur max et min """
        value_r = InfluenceMapDrawing._convert_color_value_with_minmax(value, value_min, value_max, rgb_min[0], rgb_max[0])
        value_g = InfluenceMapDrawing._convert_color_value_with_minmax(value, value_min, value_max, rgb_min[1], rgb_max[1])
        value_b = InfluenceMapDrawing._convert_color_value_with_minmax(value, value_min, value_max, rgb_min[2], rgb_max[2])
        return value_r, value_g, value_b

    @staticmethod
    def _convert_color_value_with_minmax(value, value_min, value_max, color_min, color_max):
        """ Retourne une valeur pour un dégradé de couleur en fonction de la valeur max et min """
        percentage_value = (value - value_min) / (value_max - value_min)
        if color_max > color_min:
            return int((color_max - color_min) * percentage_value + color_min)
        else:
            return int((color_min - color_max) * (1 - percentage_value) + color_max)

    @staticmethod
    def get_datain_associated():
        return DrawInfluenceMapDataIn.__name__
