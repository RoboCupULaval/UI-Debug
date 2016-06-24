# Under MIT License, see LICENSE.txt

from threading import Lock
from time import sleep, time

from PyQt4.QtCore import QThread

from Communication.UDPCommunication import UDPReceiving
from Model.DataIn.DrawingDataIn.BaseDataInDraw import BaseDataInDraw
from Model.DataIn.LoggingDataIn.BaseDataInLog import BaseDataInLog
from .DataIn.DataInFactory import DataInFactory
from .DataIn.DataInSTA import DataInSTA

__author__ = 'RoboCupULaval'


class DataInModel(object):
    def __init__(self, controller=None):
        # Initialisation
        self._controller = controller
        self._udp_receiver = UDPReceiving()
        self._datain_factory = DataInFactory()
        self._last_packet = None
        self._data_logging = list()
        self._data_config = list()
        self._data_draw = dict()
        self._data_STA = None
        self._lock = Lock()
        self._data_recovery = QThread()

        self._start_time = time()

        self._initialization()

    def _initialization(self):
        """ Initialise la structure de données du DataInModel et des threads """
        self._data_draw['notset'] = list()
        self._data_draw['robots_yellow'] = [list() for _ in range(6)]
        self._data_draw['robots_blue'] = [list() for _ in range(6)]
        self._udp_receiver.start()
        self._data_recovery.run = self._get_data_in
        self._data_recovery.start()

    def _get_data_in(self):
        while True:
            if not self._lock.locked():
                self._lock.acquire()
                try:
                    package = self._udp_receiver.get_last_data()
                    if package is not None and not package[0] == self._last_packet:
                        data_in = package[1]
                        if data_in is not None:
                            data = self._datain_factory.get_datain_object(data_in)
                            if isinstance(data, BaseDataInLog):
                                self.add_logging(data)
                            elif isinstance(data, DataInSTA):
                                if self._data_STA is not None:
                                    for key in data.data.keys():
                                        self._data_STA.data[key] = data.data[key]
                                else:
                                    self._data_STA = data
                            elif isinstance(data, BaseDataInDraw):
                                self._data_draw['notset'].append(data)
                                self.show_draw(self._data_draw['notset'][-1])
                finally:
                    self._last_packet = package[0] if package is not None else None
                    self._lock.release()
            sleep(0.01)

    def add_logging(self, data):
        self._data_logging.append(data)
        self._controller.update_logging()

    def _get_data(self, type=0):
        while True:
            if not self._lock.locked():
                self._lock.acquire()
                try:
                    if type == 1:
                        if len(self._data_logging):
                            return self._data_logging
                        else:
                            return None
                    elif type == 2:
                        if isinstance(self._data_STA, DataInSTA):
                            return self._data_STA.data
                        return None
                    elif type == 3:
                        return self._data_draw
                    else:
                        raise NotImplemented
                finally:
                    self._lock.release()
            sleep(0.005)

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
        if len(self._data_logging):
            return self._data_logging[index:]
        else:
            return None

    def show_draw(self, draw):
        if isinstance(draw, BaseDataInDraw):
            self._controller.add_draw_on_screen(draw)

    @staticmethod
    def package_is_valid(package):
        try:
            assert isinstance(package, dict)
            assert 'name' in package.keys()
            assert isinstance(package['name'], str)
            assert 'type' in package.keys()
            assert isinstance(package['type'], int)
            assert 'data' in package.keys()
            assert isinstance(package['data'], dict)
            return True
        except AssertionError:
            return False

    def save_logging(self, path):
        # TODO: Enregistrer les logs dans un fichier texte
        print(path)
