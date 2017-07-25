# Under MIT License, see LICENSE.txt

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt

__author__ = 'RoboCupULaval'


class StatusBarView(QWidget):
    def __init__(self, controller):
        super().__init__(controller)

        self._controller = controller
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self.update_loop)
        self._update_timer.start(35)

        # Labels
        self.label_coord_mouse = QLabel('')
        self.label_fps = QLabel('')

        # Initialisations
        self.init_ui()
        self.show()

    def update_loop(self):
        self.update_coord_cursor()
        self.update_fps()

    def update_fps(self):
        fps = self._controller.get_fps()
        self.label_fps.setText("[UI refresh rate: {} fps]".format(fps))

    def update_coord_cursor(self):
        x, y = self._controller.get_cursor_position_from_screen()
        self.label_coord_mouse.setText("[X: {:>5} | Y: {:>5}]".format(str(x), str(y)))

    def init_ui(self):
        self.setFixedHeight(25)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)
        layout.addWidget(self.label_fps)
        layout.addWidget(self.label_coord_mouse)

        font = QFont()
        font.setPixelSize(12)
        self.label_coord_mouse.setFont(font)
        self.label_fps.setFont(font)


