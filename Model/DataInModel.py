# Under MIT License, see LICENSE.txt

import pickle
from threading import Lock
from time import sleep, time

from PyQt4.QtCore import QMutex
from PyQt4.QtCore import QMutexLocker
from PyQt4.QtCore import QThread

from Model.DataObject.AccessorData.BaseDataAccessor import BaseDataAccessor
from Model.DataObject.AccessorData.StratGeneralAcc import StratGeneralAcc
from Model.DataObject.AccessorData.VeryLargeDataAcc import VeryLargeDataAcc
from Model.DataObject.DataFactory import DataFactory
from Model.DataObject.DrawingData.BaseDataDraw import BaseDataDraw
from Model.DataObject.LoggingData.BaseDataLog import BaseDataLog
from Model.DataObject.AccessorData.HandShakeAcc import HandShakeAcc

__author__ = 'RoboCupULaval'


class DataInModel(object):
    def __init__(self, controller=None):
        self._controller = controller

        # Stockage de données
        self._data_logging = list()
        self._data_config = list()
        self._data_draw = dict()
        self._distrib_sepcific_packet = dict()
        self._data_STA = None

        # Système interne
        self._datain_factory = DataFactory()
        self._mutex = QMutex()
        self._lock = Lock()
        self._data_recovery = QThread()
        self._start_time = time()

        # Réseau
        self._udp_receiver = None
        self._last_packet = None

        # Contrôleur
        self._pause = False

        # Initialisations
        self._init_distributor()
        self._initialization()

    def _initialization(self):
        """ Initialise la structure de données du DataInModel et des threads """
        self._data_draw['notset'] = list()
        self._data_draw['robots_yellow'] = [list() for _ in range(6)]
        self._data_draw['robots_blue'] = [list() for _ in range(6)]
        self._data_recovery.run = self._get_data_in
        self._data_recovery.start()

    def _init_distributor(self):
        """ Initialise la distribution des paquets en fonction du type de paquet """
        self._distrib_sepcific_packet[VeryLargeDataAcc.__name__] = self._distrib_VeryLargeData
        self._distrib_sepcific_packet[BaseDataDraw.__name__] = self._distrib_BaseDataDraw
        self._distrib_sepcific_packet[StratGeneralAcc.__name__] = self._distrib_StratGeneral
        self._distrib_sepcific_packet[BaseDataLog.__name__] = self._distrib_BaseDataLog
        self._distrib_sepcific_packet[HandShakeAcc.__name__] = self._distrib_HandShake

    def setup_udp_server(self, udp_server):
        """ Installer le serveur UDP """
        self._udp_receiver = udp_server
        self._udp_receiver.start()

    def _get_data_in(self):
        """ Récupère les données du serveur UDP pour les stocker dans le modèles """
        while True:
            if not self._pause:
                QMutexLocker(self._mutex).relock()
                package = None
                try:
                    package = self._udp_receiver.get_last_data()
                    self._extract_and_distribute_data(package)
                except AttributeError:
                    pass
                finally:
                    self._last_packet = package[0] if package is not None else None
                    QMutexLocker(self._mutex).unlock()
            sleep(0.01)

    def _extract_and_distribute_data(self, package):
        if package is not None:
            if isinstance(package, (tuple, list)):
                package = package[1]
            data_in = pickle.loads(package)
            if data_in is not None:
                data = self._datain_factory.get_data_object(data_in)
                try:
                    if isinstance(data, BaseDataDraw):
                        self._distrib_sepcific_packet[BaseDataDraw.__name__](data)
                    else:
                        self._distrib_sepcific_packet[type(data).__name__](data)
                except KeyError as e:
                    print(type(e).__name__, e)

    # === DISTRIBUTOR ===

    def _distrib_VeryLargeData(self, data):
        """ Traite le paquet VeryLargeData """
        data.store()
        self._extract_and_distribute_data(data.rebuild())

    def _distrib_BaseDataDraw(self, data):
        """ Traite le paquet de type générique DataDraw """
        self._data_draw['notset'].append(data)
        self.show_draw(self._data_draw['notset'][-1])

    def _distrib_StratGeneral(self, data):
        if self._data_STA is not None:
            for key in data.data.keys():
                self._data_STA.data[key] = data.data[key]
        else:
            self._data_STA = data

    def _distrib_BaseDataLog(self, data):
        self._store_data_logging(data)

    def _distrib_HandShake(self, data):
        self._controller.send_handshake()

    # === ===

    def _store_data_logging(self, data):
        """ Stock les données de logging """
        self._data_logging.append(data)
        self._controller.update_logging()

    def add_logging(self, name, message, level=2):
        data_in = {'name': name,
                   'type': 2,
                   'version': '1.0',
                   'link': None,
                   'data': {'level': level, 'message': message}
                   }
        self._store_data_logging(self._datain_factory.get_data_object(data_in))

    def _get_data(self, type=0):
        # TODO: A refactor
        QMutexLocker(self._mutex).relock()
        try:
            if type == 1:
                if len(self._data_logging):
                    return self._data_logging
                else:
                    return None
            elif type == 2:
                if isinstance(self._data_STA, StratGeneralAcc):
                    return self._data_STA.data
                return None
            elif type == 3:
                return self._data_draw
            else:
                raise NotImplemented
        finally:
            QMutexLocker(self._mutex).unlock()

    def get_last_message(self):
        try:
            return self._get_data(1)[-1]
        except BaseException:
            return None

    def get_tactics(self):
        try:
            return self._get_data(2)['T']
        except:
            return None

    def get_strats(self):
        try:
            return self._get_data(2)['S']
        except:
            return None

    def get_last_log(self, index=0):
        """ Récupère les derniers logging"""
        if len(self._data_logging):
            return self._data_logging[index:]
        else:
            return None

    def show_draw(self, draw):
        """ Afficher le dessin sur la fenêtre du terrain """
        if isinstance(draw, BaseDataDraw):
            self._controller.add_draw_on_screen(draw)

    @staticmethod
    def write_logging_file(path, text):
        """ Écrit le logging dans un fichier texte sur le path déterminé """
        with open(path, 'w') as f:
            text = '##### LOGGING FROM UI #####\n' + text
            f.write(text)

    def pause(self):
        """ Met le modèle en pause """
        self._pause = True

    def play(self):
        """ Met le modèle en lecture """
        self._pause = False

    def is_pause(self):
        """ Requete pour savoir si le modèle est en pause """
        return self._pause
