# Under GNU GPLv3 License, see LICENSE.txt

import sys, time
from random import randint
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import pyqtSignal, QMutex, QTimer

__author__ = 'jbecirovski'


class TestPainter(QWidget):
    frame_rate = 1000

    def __init__(self):
        QWidget.__init__(self)

        self.best_score = 0
        # View Screen Draws
        self._list_draw = [[randint(0, 1000), randint(0, 1000)]]
        self.setGeometry(200, 200, 1011, 720)

        # View Screen Core
        self._emit_signal = pyqtSignal()
        self._mutex = QMutex()
        self._timer = QTimer()
        self._timer.timeout.connect(self.appendItem)
        self._timer.start(1000 / TestPainter.frame_rate)
        self.show()

    def appendItem(self):
        self._emit_signal()
        self._list_draw.append([randint(0, 1000), randint(0, 1000)])
        self.refresh()

    def refresh(self):
       #QMutexLocker(self._mutex).relock()
        self.update()
        #QMutexLocker(self._mutex).unlock()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self._list_draw is not None:
            t_ref = time.time()
            for draw in self._list_draw:
                painter.setBrush(QBrush(QColor(255, 0, 0)))
                painter.setPen(QPen())
                painter.drawRect(draw[0], draw[1], 100, 100)
            t_final = (time.time() - t_ref) * 1000
            painter.drawText(100, 80, 'BEST SCORE: {}'.format(self.best_score))
            try:
                painter.drawText(100, 100, '{}| {:.0f} ms | {:.0f} hertz| {:.4f} dbms'.format(len(self._list_draw), t_final, 1 / (t_final/1000), len(self._list_draw) / t_final))
                if 1 / (t_final / 1000) < 30:
                    self.best_score = len(self._list_draw)
                    self._list_draw.clear()
            except Exception as e:
                pass
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    f = TestPainter()
    f.show()
    sys.exit(app.exec_())
