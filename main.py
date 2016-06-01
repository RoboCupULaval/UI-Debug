# Under MIT License, see LICENSE.txt
import sys
from PyQt4.QtGui import QApplication
from View.MainWindow import MainWindow

__author__ = 'RoboCupULaval'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    f = MainWindow()
    f.show()
    sys.exit(app.exec_())
