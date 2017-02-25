# Under MIT License, see LICENSE.txt
import sys

import Controller.config as config
try:
    config_mode = sys.argv[1]
except IndexError:
    config_mode = "simulation"
config.set_config(config_mode)

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


