# Under MIT License, see LICENSE.txt
import sys

#try:
from PyQt5.QtWidgets import QApplication
from Controller.MainController import MainController
#except ImportError:
#    sys.stderr.write("PyQt5 n'est pas bien installé sur votre ordinateur. Veuillez installer une des versions " +
#                     "disponibles sur https://sourceforge.net/projects/pyqt/files/PyQt5/\n")

__author__ = 'RoboCupULaval'

if __name__ == '__main__':
    #try:
    app = QApplication(sys.argv)
    f = MainController()
    f.show()
    sys.exit(app.exec_())
    #except NameError:
    #    pass


