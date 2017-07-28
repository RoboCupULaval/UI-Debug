# Under MIT License, see LICENSE.txt
import sys
import argparse
import warnings
from configparser import ParsingError, ConfigParser

from PyQt5.QtWidgets import QApplication
from qtpy import QtCore

from Controller.MainController import MainController

__author__ = 'RoboCupULaval'

def argumentParser(argument):
    """ Argument parser """
    parser = argparse.ArgumentParser(description='option pour initialiser le UI-debug')
    parser.add_argument('use_type', metavar='use_type', type=str, default='../StrategyIA/config/field/sim.cfg',
                        help='use_type = sim: utilise les data de grsim dans le port 10024 (il faut set le port de '
                             'grsim a 10024 pour que ca marche) use_type = real: utilise le port normal de la '
                             'vision (10020)')
    parser.add_argument('team_color', metavar='team_color', type=str, default='blue',
                        help='team_color, set the color to use for the ports')
    args_ = parser.parse_args(argument)
    return args_

def load_config(path):
    config_parser = ConfigParser(allow_no_value=False)
    try:
        print("Loading", path, " port configuration file.")
        config_parser.read_file(open(path))
    except FileNotFoundError:
        raise RuntimeError("Impossible de lire le fichier de configuration.")
    except ParsingError:
        raise RuntimeError("Le fichier de configuration est mal configuré.\nExiting!")

    return {s: dict(config_parser.items(s)) for s in config_parser.sections()}["COMMUNICATION"]

if __name__ == '__main__':
    args = argumentParser(None)
    app = QApplication(sys.argv)

    config = load_config(args.use_type)

    if args.team_color == "blue":
        ui_cmd_sender_port = 14444
        ui_cmd_receiver_port = 15555
    else:
        ui_cmd_sender_port = 16666
        ui_cmd_receiver_port = 17777

    f = MainController(int(config["vision_port"]), int(config["referee_port"]), ui_cmd_sender_port, ui_cmd_receiver_port)
    f.show()
    sys.exit(app.exec_())
    #except NameError:
    #    pass
