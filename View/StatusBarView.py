# Under MIT License, see LICENSE.txt

from PyQt4 import QtGui
from PyQt4 import QtCore

__author__ = 'RoboCupULaval'


class StatusBarView(QtGui.QWidget):
    def __init__(self, controller):
        super().__init__(controller)

        self._controller = controller
        self._update_timer = QtCore.QTimer()
        self._update_timer.timeout.connect(self.update_loop)
        self._update_timer.start(35)

        # Labels
        self.label_coord_mouse = QtGui.QLabel('')

        # Initialisations
        self.init_ui()
        self.show()

    def update_loop(self):
        self.update_coord_cursor()

    def update_coord_cursor(self):
        x, y = self._controller.get_cursor_position_from_screen()
        self.label_coord_mouse.setText("X: {: >5} | Y: {: >5}".format(str(x), str(y)))

    def init_ui(self):
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(QtCore.Qt.AlignLeft)
        layout.setAlignment(QtCore.Qt.AlignVCenter)
        self.setLayout(layout)
        layout.addWidget(self.label_coord_mouse)

        font = QtGui.QFont()
        font.setPixelSize(12)
        self.label_coord_mouse.setFont(font)


