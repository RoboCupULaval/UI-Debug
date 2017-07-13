# Under MIT License, see LICENSE.txt
import sys
import argparse



from PyQt5.QtWidgets import QApplication
from qtpy import QtCore

from Controller.MainController import MainController

__author__ = 'RoboCupULaval'

def argumentParser(argument):
    """ Argument parser """
    parser = argparse.ArgumentParser(description='option pour initialiser le UI-debug')
    parser.add_argument('use_type', metavar='use_type', type=str, default='sim',
                        help='use_type = sim: utilise les data de grsim dans le port 10024 (il faut set le port de '
                             'grsim a 10024 pour que ca marche) use_type = real: utilise le port normal de la '
                             'vision (10020)')
    parser.add_argument('team_color', metavar='team_color', type=str, default='blue',
                        help='team_color, soit blue (default) ou yellow')
    args_ = parser.parse_args(argument)
    return args_

if __name__ == '__main__':
    args = argumentParser(None)
    app = QApplication(sys.argv)
    if args.use_type == 'sim':
        port = 10024
    else:
        port = 10020
    if args.team_color == 'blue':
        ui_cmd_rcv_port = 20021
    else:
        ui_cmd_rcv_port = 20031

    f = MainController(port, ui_cmd_rcv_port)
    f.show()
    sys.exit(app.exec_())
    #except NameError:
    #    pass