# Under MIT License, see LICENSE.txt

from PyQt4.QtGui import QPixmap
from Controller.MobileObject.BaseMobileObject import BaseMobileObject
from Controller.QtToolBox import QtToolBox
__author__ = 'RoboCupULaval'


class TargetMob(BaseMobileObject):
    def __init__(self, x=0, y=0):
        BaseMobileObject.__init__(self, x, y)
        self._size = 250
        self._path = 'Img/ico-target.png'
        self._pixmap_obj = QPixmap(self._path)

    def draw(self, painter):
        if self.isVisible():
            size = self._size * QtToolBox.field_ctrl.ratio_screen
            x, y, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(self._x, self._y)
            painter.drawPixmap(x - size / 2, y - size / 2, size, size, self._pixmap_obj)

    @staticmethod
    def get_qt_item(drawing_data_in):
        pass

    @staticmethod
    def get_datain_associated():
        return 'target'

