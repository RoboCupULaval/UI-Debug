# Under MIT License, see LICENSE.txt
import sys
import argparse
import warnings


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
    args_ = parser.parse_args(argument)
    return args_

if __name__ == '__main__':
    args = argumentParser(None)
    app = QApplication(sys.argv)
    if args.use_type == 'sim':
        port = 10024
    elif args.use_type == 'kalman':
        port = 10022
    elif args.use_type == 'real':
        port = 10026
    else:  # force real-life
        warnings.warn("Unrecognized use_type argument. force real-life.", SyntaxWarning, stacklevel=2)
        port = 10020

    f = MainController(port)
    f.show()
    sys.exit(app.exec_())
    #except NameError:
    #    pass
