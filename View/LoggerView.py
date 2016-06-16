# Under MIT License, see LICENSE.txt

from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton
from Model.DataInModel import DataInModel

__author__ = 'RoboCupULaval'


class LoggerView(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._parent = parent
        self._model = None
        self._count = 0
        self.pause = False
        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(200)
        self.log_queue = QListWidget(self)
        layout = QHBoxLayout()
        layout.addWidget(self.log_queue)

        layout_btn = QVBoxLayout()
        self.btn_pause = QPushButton('Pause')
        self.btn_pause.setCheckable(True)
        self.btn_pause.setChecked(self.pause)
        self.btn_pause.clicked.connect(self.pauseEvent)
        layout_btn.addWidget(self.btn_pause)
        layout.addLayout(layout_btn)

        self.setLayout(layout)

        self.hide()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_logger)
        self.timer.start(250)

    def pauseEvent(self):
        self.pause = not self.pause
        self.btn_pause.setChecked(self.pause)

    def set_model(self, model):
        if isinstance(model, DataInModel):
            self._model = model
        else:
            raise TypeError('Logger should get data in model argument.')

    def update_logger(self):
        if not self.pause:
            if self._model is not None:
                messages = self._model.get_last_log(self._count)
                if messages is not None:
                    self._count += len(messages)
                    for msg in messages:
                        self.log_queue.addItem(str(msg))
                    self.log_queue.scrollToBottom()

    def get_count(self):
        return self._count

    def show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self._parent.resize_window()
