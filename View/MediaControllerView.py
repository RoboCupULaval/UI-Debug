# Under MIT License, see LICENSE.txt

from time import time
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

__author__ = 'RoboCupULaval'


class MediaControllerView(QtGui.QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Vue
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        button_layout = QtGui.QHBoxLayout()
        self._media_slider = QtGui.QSlider(self)
        self._media_slider.setOrientation(Qt.Horizontal)
        layout.addLayout(button_layout)
        layout.addWidget(self._media_slider)

        self._but_play = QtGui.QPushButton('>')
        self._but_play.setFixedSize(20, 20)
        self._but_backward = QtGui.QPushButton('|<')
        self._but_backward.setFixedSize(20, 20)
        self._but_forward = QtGui.QPushButton('>|')
        self._but_forward.setFixedSize(20, 20)
        button_layout.addWidget(self._but_backward)
        button_layout.addWidget(self._but_play)
        button_layout.addWidget(self._but_forward)

        # Paramètres de temps
        self._time_width = 30
        self._time_min = 0
        self._time_max = 0
        self._time_cursor = 0

        self.hide()

    def pause(self):
        self.controller.pause_models()

    def play(self):
        self.controller.play_models()

    def auto_set_timeline(self):
        self._time_max = time()
        self._time_min = self._time_max - self._time_width
        self._time_cursor = self._time_max

    def toggle_visibility(self):
        if self.isVisible():
            self.play()
            self.hide()
        else:
            self.pause()
            self.show()
