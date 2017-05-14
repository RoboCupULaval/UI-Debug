# Under MIT License, see LICENSE.txt
import sys




from PyQt5.QtWidgets import QApplication
from Controller.MainController import MainController

__author__ = 'RoboCupULaval'

if __name__ == '__main__':
    #try:

    app = QApplication(sys.argv)
    f = MainController()
    f.show()
    sys.exit(app.exec_())
    #except NameError:
    #    pass


