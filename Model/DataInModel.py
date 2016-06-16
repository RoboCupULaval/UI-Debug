# Under MIT License, see LICENSE.txt

from time import sleep, time
from threading import Thread, Lock
from Communication.UDPCommunication import UDPReceiving
from .DataIn.DataIn import DataIn
from .DataIn.DataInFactory import DataInFactory, DataInLog, DataInSTA


__author__ = 'RoboCupULaval'


class DataInModel(object):
    def __init__(self):
        # Initialisation
        self._udp_receiver = UDPReceiving()
        self._last_packet = None
        self._data_logging = list()
        self._data_config = list()
        self._data_STA = None
        self._lock = Lock()
        self._data_recovery = Thread(target=self._get_data_in, daemon=True)

        self._start_time = time()

        self._initialization()

    def _initialization(self):

        self._udp_receiver.start()
        self._data_recovery.start()

    def _get_data_in(self):
        while True:
            if not self._lock.locked():
                self._lock.acquire()
                try:
                    package = self._udp_receiver.get_last_data()
                    if package is not None and not package[0] == self._last_packet:
                        data_in = package[1]
                        if data_in is not None and self.package_is_valid(data_in):
                            data = DataInFactory.get_data(data_in['name'], data_in['type'], data_in['data'])
                            if isinstance(data, DataInLog):
                                self._data_logging.append(data)
                            elif isinstance(data, DataInSTA):
                                if self._data_STA is not None:
                                    for key in data.data.keys():
                                        self._data_STA.data[key] = data.data[key]
                                else:
                                    self._data_STA = data
                finally:
                    self._last_packet = package[0] if package is not None else None
                    self._lock.release()
            sleep(0.01)

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

    @staticmethod
    def package_is_valid(package):
        try:
            return True
            # TODO: Faire vérification du paquet
            return DataIn.package_is_valid(package['name'], package['type'])
        except KeyError:
            return False
