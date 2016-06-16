# Under MIT License, see LICENSE.txt

from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QSize
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

        layout_btn = QVBoxLayout()
        self.btn_media_ctrl = QPushButton()
        self.btn_media_ctrl.setIcon(QIcon('Img/control_pause.png'))
        self.btn_media_ctrl.setIconSize(QSize(16, 16))
        self.btn_media_ctrl.setDisabled(True)
        self.btn_media_ctrl.setCheckable(False)
        self.btn_media_ctrl.clicked.connect(self.pauseEvent)
        layout_btn.addWidget(self.btn_media_ctrl)

        # Initialisation Layout
        layout.addLayout(layout_btn)
        layout.addWidget(self.log_queue)

        self.setLayout(layout)

        self.hide()

    def pauseEvent(self):
        self.pause = not self.pause
        if self.pause:
            self.btn_media_ctrl.setIcon(QIcon('Img/control_play.png'))
        else:
            self.btn_media_ctrl.setIcon(QIcon('Img/control_pause.png'))

    def set_model(self, model):
        if isinstance(model, DataInModel):
            self._model = model
        else:
            raise TypeError('Logger should get data in model argument.')

    def refresh(self):
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

    def clear(self):
        # TODO : Clear la liste des logs
        pass

    def save(self):
        # TODO : Sauvegarde sous forme de texte les logs
        pass

    def show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self._parent.resize_window()
